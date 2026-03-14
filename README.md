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

Madhan Kumar
