import boto3
import os

def aws_setup_config():

  session = boto3.Session(
      aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
      aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
  return session

def next_option():
    while True:
        ask = input("\nType 'yes' to procced to the next option: ")
        if ask == "yes":
          os.system('clear')
          break
        else:
          print("\nInvalid option")