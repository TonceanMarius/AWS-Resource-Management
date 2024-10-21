import boto3
from other_functions import aws_setup_config
import os

class SNSOperations:
    def __init__(self):
        self.session = aws_setup_config()
        self.sns_operations = self.session.client('sns', region_name=os.getenv('AWS_REGION'))

    def sns_post(self):
    
       sns_arn = "arn:aws:sns:eu-central-1:381492036418:S3_SNS"
       self.sns_operations.publish(TopicArn=sns_arn, Message="S3 file distribution completed")