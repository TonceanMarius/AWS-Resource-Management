from typing import Self
from botocore.exceptions import ClientError
import boto3
import os
from other_functions import aws_setup_config

#working perfectly

class EC2Operations:

  def __init__(self):
    self.session = aws_setup_config()
    self.ec2_operations = self.session.client('ec2', region_name=os.getenv('AWS_REGION'))
    
  def ec2_creation(self):

    list_ec2 = self.check_status_ec2()
    if  not list_ec2:
      list_ec2 = []
    ask_ec2 = input("\nPlease introduce the name of the new ec2 that you want to create or quit (q): ")
    if ask_ec2 not in list_ec2 and ask_ec2 != 'q':
      self.ec2_operations.run_instances(ImageId='ami-00f07845aed8c0ee7',
                                      MinCount=1,
                                      MaxCount=1,
                                      InstanceType='t2.micro',
                                      KeyName='key_code',
                                      SecurityGroupIds=['sg-07382c1210fc556e7'],
                                      TagSpecifications=[{
                                          'ResourceType':
                                          'instance',
                                          'Tags': [{
                                              'Key': 'Name',
                                              'Value': ask_ec2
                                          }]
                                      }])    
      
      print(f"\nThe EC2 instance {ask_ec2} has been successfully created")
    elif ask_ec2 == "q":
      pass
    elif ask_ec2 in list_ec2:
      print(f"\nThe EC2 instance '{ask_ec2}' couldn't be created, it already exists")

  def check_status_ec2(self):

    response = self.ec2_operations.describe_instances()
    name_ec2 = []
    status_ec2 = []
    list_ec2 = []
    
    if response['Reservations'] != None:
      for reservation in response['Reservations']:
        for instance in reservation['Instances']:
          status = instance['State']['Name']
          status_ec2.append(status)
    
          instance_name = None
          for tag in instance.get('Tags', []):
            if tag['Key'] == 'Name':
              instance_name = tag['Value']
              break
    
          name_ec2.append(instance_name)
      
      for name, status in zip(name_ec2, status_ec2):
        print(f"\nInstance Name: {name}, Status: {status}")
        list_ec2.append(name)
      return list_ec2
    else:
      print("\nThere are no EC2 instances available\n")

  def stop_ec2(self):

    list_ec2 = self.check_status_ec2()
    if  not list_ec2:
      list_ec2 = []
    response = self.ec2_operations.describe_instances()
    ask_ec2_stop = input("\nPlease tell the EC2 name you want to stop or quit (q): ")
    
    if ask_ec2_stop != 'q' and ask_ec2_stop in list_ec2:
      for reservation in response['Reservations']:
        for instance in reservation['Instances']:
          for tag in instance['Tags']:
            if (tag['Key'] == "Name" and tag['Value'] == ask_ec2_stop
                and (instance['State']['Name'] == 'running'
                     or instance['State']['Name'] == 'pending')):
              try:
                self.ec2_operations.stop_instances(InstanceIds=[instance['InstanceId']],
                                   DryRun=False)
                print(f"\nThe EC2 {ask_ec2_stop} has been successfully stopped")
              except ClientError as e:
                print(e)
    
            elif (tag['Key'] == 'Name' and tag['Value'] == ask_ec2_stop
                  and instance['State']['Name'] == 'stopped'):
              print(f"\nThe EC2 instance {ask_ec2_stop}"
                    f" has already been stopped")
    
            elif (tag['Key'] == 'Name' and tag['Value'] == ask_ec2_stop
                  and instance['State']['Name'] == 'stopping'):
              print(f"\nThe EC2 instance {ask_ec2_stop}"
                    f" is currently stopping")
    
            elif (tag['Key'] == 'Name' and tag['Value'] == ask_ec2_stop
                  and instance['State']['Name'] == 'terminated'):
              print(f"\nThe EC2 instance {ask_ec2_stop} can't be stopped,"
                    f" it has already been terminated")
    
            elif (tag['Key'] == 'Name' and tag['Value'] == ask_ec2_stop
                  and instance['State']['Name'] == 'shutting-down'):
              print(f"\nThe EC2 instance {ask_ec2_stop}"
                    f" is currently shutting down")
          
    elif ask_ec2_stop not in list_ec2 and ask_ec2_stop != "q":
      print("\nThe EC2 instance you want to stop doesn't exists")
    elif ask_ec2_stop == "q":
      pass
    else:
      print("Please give a valid option")

  def start_ec2(self):

    list_ec2 = self.check_status_ec2()
    if  not list_ec2:
      list_ec2 = []
    name_ec2 = input("\nPlease introduce the name of the EC2 you want to start quit (q): ")
    response = self.ec2_operations.describe_instances()

    if name_ec2 != 'q' and name_ec2 in list_ec2:
      for reservation in response['Reservations']:
        for instance in reservation['Instances']:
          for tag in instance['Tags']:
            if (tag['Key'] == 'Name' and tag['Value'] == name_ec2
                and instance['State']['Name'] == 'stopped'):
              try:
                (self.ec2_operations.start_instances(InstanceIds=[instance['InstanceId']],
                                     DryRun=False))
                print(f"\nThe EC2 instance {name_ec2}"
                      f" has been successfully started")
              except ClientError as e:
                print(e)
    
            elif (tag['Key'] == 'Name' and tag['Value'] == name_ec2
                  and instance['State']['Name'] == 'running'):
              print(f"\nThe EC2 instance {name_ec2}"
                    f" is currently running")
    
            elif (tag['Key'] == 'Name' and tag['Value'] == name_ec2
                  and instance['State']['Name'] == 'pending'):
              print(f"\nThe EC2 instance {name_ec2}"
                    f" is currently pending")
              
            elif (tag['Key'] == 'Name' and tag['Value'] == name_ec2
                  and instance['State']['Name'] == 'stopping'):
              print(f"\nThe EC2 instance {name_ec2}"
                    f" is currently stopping")
    
            elif (tag['Key'] == 'Name' and tag['Value'] == name_ec2
                  and instance['State']['Name'] == 'terminated'):
              print(f"\nThe EC2 instance {name_ec2} can't be started,"
                    f" it has already been terminated")
    
            elif (tag['Key'] == 'Name' and tag['Value'] == name_ec2
                  and instance['State']['Name'] == 'shutting-down'):
              print(f"\nThe EC2 instance {name_ec2}"
                    f" is currently shutting down")
              
    elif name_ec2 not in list_ec2 and name_ec2 != "q":
      print("\nThe EC2 instance you want to start doesn't exists")
    elif name_ec2 == "q":
      pass
    else:
      print("Please give a valid option")
  
  def terminate_ec2(self):

    list_ec2 = self.check_status_ec2()
    if  not list_ec2:
      list_ec2 = []
    name_ec2 = input("\nPlease tell the EC2 you want to terminate or quit (q): ")
    response = self.ec2_operations.describe_instances()
    if name_ec2 != 'q' and name_ec2 in list_ec2:
      for reservation in response['Reservations']:
        for instance in reservation['Instances']:
          for tag in instance['Tags']:
            if (tag['Key'] == 'Name' and tag['Value'] == name_ec2
                and instance['State']['Name'] != 'terminated'):
              try:
                (self.ec2_operations.terminate_instances(InstanceIds=[instance['InstanceId']]))
                print(f"\nThe EC2 instance {name_ec2}"
                      f" has been successfully terminated")
              except ClientError as e:
                print(e)
    
            elif (tag['Key'] == 'Name' and tag['Value'] == name_ec2
                  and instance['State']['Name'] == 'terminated'):
              print(f"\nThe EC2 instance {name_ec2}"
                    f" has already been terminated")
            
    elif name_ec2 not in list_ec2 and name_ec2 != "q":
      print("\nThe EC2 instance you want to terminate doesn't exists")
    elif name_ec2 == "q":
      pass
    else:
      print("Please give a valid option")

  def reboot_ec2(self):

    list_ec2 = self.check_status_ec2()
    if  not list_ec2:
      list_ec2 = []
    name_ec2 = input("\nPlease introduce the name of the ec2 you want to reboot or quit (q): ")
    response = self.ec2_operations.describe_instances()
    if name_ec2 != 'q' and name_ec2 in list_ec2:
      for reservation in response['Reservations']:
        for instance in reservation['Instances']:
          for tag in instance['Tags']:
            if (tag['Key'] == 'Name' and tag['Value'] == name_ec2
                and instance['State']['Name'] != 'terminated' 
                  and instance['State']['Name'] != 'stopped'):
              try:
                self.ec2_operations.reboot_instances(InstanceIds=[instance['InstanceId']])
                print(f"\nThe EC2 instance {name_ec2}"
                      f" has been successfully rebooted")
              except ClientError as e:
                print(e)
            elif (tag['Key'] == 'Name' and tag['Value'] == name_ec2
                  and instance['State']['Name'] == 'stopped'):
              print(f"\nThe EC2 instance {name_ec2}"
                    f" can't be rebooted, it is in stopped state")
            elif (tag['Key'] == 'Name' and tag['Value'] == name_ec2
                  and instance['State']['Name'] == 'terminated'):
              print(f"\nThe EC2 instance {name_ec2} can't been rebooted"
                    f" it has been termianted")
            
    elif name_ec2 not in list_ec2 and name_ec2 != "q":
      print("\nThe EC2 instance you want to reboot doesn't exists")
    elif name_ec2 == "q":
      pass
    else:
      print("Please give a valid option")

  def info_ec2(self):

    list_ec2 = self.check_status_ec2()
    if  not list_ec2:
      list_ec2 = []
    ask_info = input("\nPlease introduce the name of the instance you want info for or quit (q): ")
    response = self.ec2_operations.describe_instances()
    if ask_info in list_ec2 and ask_info != 'q':
      for res in response['Reservations']:
        for res1 in res['Instances']:
          for res2 in res1['Tags']:
            if res2['Value'] == ask_info:
              print(f"\nInstance Name: {res1['Tags'][0]['Value']}\n")
              print(f"Instance Status: {res1['State']['Name']}\n")
              print(f"Instance ID: {res1['InstanceId']}\n")
              print(f"Instance OS: {res1['PlatformDetails']}\n")
              print(f"Instance type: {res1['InstanceType']}\n")
              if 'PublicIpAddress' in res1 and res1['PublicIpAddress'] is not None:
                print(f"Instance Public IP: {res1['PublicIpAddress']}\n")
              else:
                print("Instance Public IP: N/A\n")
              print(
                  f"Instance Availability Zone: {res1['Placement']['AvailabilityZone']}"
              )
              
    elif ask_info not in list_ec2 and ask_info != 'q':
      print("\nThe EC2 instance you want to access information doesn't exists")
    elif ask_info == "q":
      pass