# Automated EC2 Disaster Recovery Backup

This project automates EC2 backup using AWS Lambda.

## Architecture

EventBridge Scheduler triggers Lambda daily.

Lambda performs:
- Identify EC2 instances with tag `Backup=true`
- Create EBS snapshots
- Store backup metadata in S3
- Send notifications using SNS
- Delete old snapshots based on retention policy

## AWS Services Used

- AWS Lambda
- Amazon EC2
- Amazon EBS Snapshots
- Amazon S3
- Amazon SNS
- EventBridge Scheduler
- IAM

## Project Flow

EventBridge Scheduler  
→ Lambda  
→ Create EBS Snapshot  
→ Store Manifest in S3  
→ Send Email via SNS  
→ Delete old snapshots

## Features

- Automated EC2 backup
- Tag-based backup selection
- Snapshot retention policy
- Email notifications
- Backup metadata storage

## Screenshots

Add screenshots of:
- Lambda configuration
- Snapshot creation
- EventBridge scheduler
- S3 manifest
- SNS email alert

## Author


# Step-by-Step Implementation

## Step 1: Create S3 Bucket

Create an S3 bucket to store backup manifest files.

Example bucket name:


madhan-ec2-dr-backup-metadata


Create folders inside the bucket:


manifests/
logs/
recovery/
reports/


---

## Step 2: Create SNS Topic

Create an SNS topic to receive backup notifications.

Topic name:


ec2-backup-alerts


Add email subscription.

Confirm the subscription from your email inbox.

---

## Step 3: Create IAM Role for Lambda

Create an IAM role for Lambda.

Role name:


lambda-ec2-backup-role


Attach these policies:


AmazonEC2FullAccess
AmazonS3FullAccess
AmazonSNSFullAccess
CloudWatchLogsFullAccess


---

## Step 4: Create Lambda Function

Create a Lambda function.

Function name:


ec2-snapshot-backup


Runtime:


Python 3.x


Attach IAM role created earlier.

---

## Step 5: Add Lambda Environment Variables

Add environment variables in Lambda configuration.


BUCKET_NAME = madhan-ec2-dr-backup-metadata
SNS_TOPIC_ARN = your-sns-topic-arn
BACKUP_TAG_KEY = Backup
BACKUP_TAG_VALUE = true


---

## Step 6: Add EC2 Instance Tag

Add the following tag to the EC2 instance.


Key = Backup
Value = true


This ensures only selected instances are backed up.

---

## Step 7: Add Lambda Backup Code

Upload the backup automation script inside:


lambda/lambda_function.py


The Lambda function performs:

- EC2 instance discovery
- EBS volume detection
- Snapshot creation
- Backup manifest storage in S3
- SNS notification
- Snapshot cleanup

---

## Step 8: Test Lambda Function

Create a test event.


{}


Run the Lambda function.

Expected output:

- Snapshot created
- S3 manifest file created
- SNS email notification received

---

## Step 9: Verify Backup

Verify the following resources.

### EC2 Snapshots

Navigate to:


EC2 → Snapshots


Confirm new snapshot exists.

---

### S3 Manifest File

Navigate to:


S3 → madhan-ec2-dr-backup-metadata → manifests/


Confirm JSON manifest file.

---

### SNS Email Notification

Check email inbox for backup notification.

---

### CloudWatch Logs

Navigate to:


CloudWatch → Log Groups → /aws/lambda/ec2-snapshot-backup


Confirm Lambda execution logs.

---

## Step 10: Configure Daily Automation

Open **EventBridge Scheduler**.

Create schedule.

Schedule name:


ec2-daily-snapshot-backup


Schedule type:


Recurring


Cron expression:


cron(0 2 * * ? *)


This runs backup daily at **2:00 AM**.

Target:


Lambda → ec2-snapshot-backup


Input:


{}


---

## Step 11: Configure Snapshot Retention Policy

Retention logic is implemented inside Lambda.

Example policy:


Keep snapshots for 7 days
Delete snapshots older than 7 days


This prevents unnecessary storage costs.

---

# Final Architecture Flow


EventBridge Scheduler
│
▼
Lambda Function
│
▼
EBS Snapshots
│
┌───────────────┬───────────────┐
▼ ▼
S3 Manifest SNS Email Alert


---

# Project Features

- Automated EC2 backup
- Tag-based instance selection
- EBS snapshot automation
- Backup metadata stored in S3
- Email alert system using SNS
- Scheduled backups using EventBridge
- Snapshot retention policy
- Disaster recovery ready architecture
