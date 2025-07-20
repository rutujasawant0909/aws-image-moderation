import boto3
import json
import os

rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')
sns = boto3.client('sns')

SAFE_BUCKET = os.environ['SAFE_BUCKET']
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    try:
        # Get uploaded image info
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        response = rekognition.detect_moderation_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': key}},
            MinConfidence=80
        )

        labels = response['ModerationLabels']
        print(f"Detected labels: {labels}")

        if not labels:
            # Safe image — copy to SAFE_BUCKET
            copy_source = {'Bucket': bucket, 'Key': key}
            s3.copy_object(Bucket=SAFE_BUCKET, CopySource=copy_source, Key=key)
            print("Image marked safe and copied to safe bucket.")
        else:
            # Unsafe — notify via SNS
            label_names = [label['Name'] for label in labels]
            message = f"Image '{key}' is flagged as unsafe. Labels: {label_names}"

            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="Unsafe Image Detected",
                Message=message
            )
            print("Unsafe image detected and SNS notification sent.")

        return {
            'statusCode': 200,
            'body': json.dumps({'result': 'processed', 'unsafe': bool(labels)})
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
