import json
import os
from datetime import datetime, timedelta
import boto3

ec2 = boto3.client("ec2")
s3 = boto3.client("s3")
sns = boto3.client("sns")

BUCKET_NAME = os.environ["BUCKET_NAME"]
SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]
BACKUP_TAG_KEY = os.environ.get("BACKUP_TAG_KEY", "Backup")
BACKUP_TAG_VALUE = os.environ.get("BACKUP_TAG_VALUE", "true")

RETENTION_DAYS = 7


def lambda_handler(event, context):

    backup_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    results = []

    try:

        response = ec2.describe_instances(
            Filters=[
                {"Name": f"tag:{BACKUP_TAG_KEY}", "Values": [BACKUP_TAG_VALUE]},
                {"Name": "instance-state-name", "Values": ["running", "stopped"]}
            ]
        )

        reservations = response.get("Reservations", [])

        for reservation in reservations:
            for instance in reservation.get("Instances", []):

                instance_id = instance["InstanceId"]
                volume_ids = []

                for mapping in instance.get("BlockDeviceMappings", []):
                    ebs = mapping.get("Ebs")
                    if ebs:
                        volume_ids.append(ebs["VolumeId"])

                instance_result = {
                    "instance_id": instance_id,
                    "volumes": []
                }

                for volume_id in volume_ids:

                    snap = ec2.create_snapshot(
                        VolumeId=volume_id,
                        Description=f"Automated backup for {instance_id}",
                        TagSpecifications=[
                            {
                                "ResourceType": "snapshot",
                                "Tags": [
                                    {"Key": "CreatedBy", "Value": "LambdaBackup"},
                                    {"Key": "InstanceId", "Value": instance_id},
                                ],
                            }
                        ],
                    )

                    snapshot_id = snap["SnapshotId"]

                    instance_result["volumes"].append({
                        "volume_id": volume_id,
                        "snapshot_id": snapshot_id
                    })

                results.append(instance_result)

        # -------- SNAPSHOT RETENTION --------

        delete_before = datetime.utcnow() - timedelta(days=RETENTION_DAYS)

        snapshots = ec2.describe_snapshots(
            OwnerIds=["self"]
        )["Snapshots"]

        deleted_snapshots = []

        for snap in snapshots:

            tags = {t["Key"]: t["Value"] for t in snap.get("Tags", [])}

            if tags.get("CreatedBy") == "LambdaBackup":

                if snap["StartTime"].replace(tzinfo=None) < delete_before:

                    ec2.delete_snapshot(SnapshotId=snap["SnapshotId"])

                    deleted_snapshots.append(snap["SnapshotId"])

        manifest = {
            "backup_time": backup_time,
            "instances": results,
            "deleted_snapshots": deleted_snapshots
        }

        s3_key = f"manifests/{datetime.utcnow().strftime('%Y/%m/%d')}/backup.json"

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=json.dumps(manifest, indent=2),
            ContentType="application/json"
        )

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="EC2 Backup Completed",
            Message=json.dumps(manifest, indent=2)
        )

        return {
            "statusCode": 200,
            "body": json.dumps(manifest)
        }

    except Exception as e:

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="EC2 Backup Failed",
            Message=str(e)
        )

        return {
            "statusCode": 500,
            "body": str(e)
        }
