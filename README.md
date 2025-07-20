# Smart Image Moderation System (AWS Rekognition + Lambda)

This serverless project automatically scans images uploaded to an S3 bucket and detects inappropriate content using AWS Rekognition. Safe images are copied to a safe bucket; unsafe ones trigger an SNS alert.

##Tech Stack

- AWS Lambda
- Amazon Rekognition (AI content moderation)
- Amazon S3 (file storage)
- Amazon SNS (notification)
- AWS SAM
- Python (boto3)

## Workflow

1. Upload image to incoming-images-moderation bucket
2. Lambda function is triggered
3. Image is scanned with Rekognition
4. Safe ➝ copied to safe-images-moderation  
   Unsafe ➝ email/SMS sent via SNS

# Folder Structure
