from dynamodb import DynamoDB_Operations
from s3_operations import S3Operations
from sns_operations import SNSOperations
from ec2_operations import EC2Operations
from other_functions import next_option
import time, os


def dynamodb_menu():

  dynamodb_class = DynamoDB_Operations()

  menu_dynamodb = {
      "1)": "Create DynamoDB table",
      "2)": "Delete DynamoDB table",
      "3)": "List DynamoDB tables",
      "4)": "Check content from DynamoDB tables",
      "5)": "Insert content in DynamoDB tables",
      "6)": "Delete content from DynamoDB tables",
      "7)": "Return to the main menu"
  }

  while True:
    
    for key, value in menu_dynamodb.items():
      print(f"{key} {value}")
      
    ask_option = input("\nPlease select the operation you "\
                       "want to execute on the DynamoDB service: ")
    
    if ask_option == "1":
      dynamodb_class.dynamodb_create()
      next_option()
      
    elif ask_option == "2":
      dynamodb_class.dynamodb_delete()
      next_option()
      
    elif ask_option == "3":
      dynamodb_class.dynamodb_list()
      next_option()
      
    elif ask_option == "4":
      dynamodb_class.check_table_items()
      next_option()
      
    elif ask_option == "5":
      dynamodb_class.insert_item()
      next_option()
      
    elif ask_option == "6":
      dynamodb_class.delete_items()
      next_option()
      
    elif ask_option == '7':
      print("Returning to the main menu...")
      time.sleep(1)
      os.system('clear')
      break
      
    else:
      print("Invalid option!") 
      time.sleep(1)
      os.system('clear')

def ec2_menu():

  ec2_class = EC2Operations()

  menu_ec2 = {
      "1)": "Check the status of the ec2 instances",
      "2)": "Create an EC2 instance",
      "3)": "Start an EC2 instance",
      "4)": "Stop an EC2 instance",
      "5)": "Reboot an EC2 instance",
      "6)": "Terminate an EC2 instance",
      "7)": "Show information about an EC2 instance",
      "8)": "Return to the main menu"
  }

  while True:

    for key, value in menu_ec2.items():
      print(f"{key} {value}")
    
    ask_option = input("\nPlease select the operation you "\
       "want to execute on the EC2 service: ")
    
    if ask_option == "1":
      ec2_class.check_status_ec2()
      next_option()
        
    elif ask_option == "2":
      ec2_class.ec2_creation()
      next_option()
      
    elif ask_option == "3":
      ec2_class.start_ec2()
      next_option()
        
    elif ask_option == "4":
      ec2_class.stop_ec2()
      next_option()
        
    elif ask_option == "5":
      ec2_class.reboot_ec2()
      next_option()
        
    elif ask_option == "6":
      ec2_class.terminate_ec2()
      next_option()
        
    elif ask_option == "7":
      ec2_class.info_ec2()
      next_option()
      
    elif ask_option == "8":
      print("Returning to the main menu...")
      time.sleep(1)
      os.system('clear')
      break
      
    else:
      print("Invalid option!") 
      time.sleep(1)
      os.system('clear')


def s3_menu():

  s3_class = S3Operations()
  sns_class = SNSOperations()

  menu_s3 = {
      "1)": "Distribute the S3 content in its respective buckets",
      "2)": "Create an S3 bucket",
      "3)": "Delete an S3 bucket",
      "4)": "List the S3 buckets",
      "5)": "List the objects in an S3 bucket",
      "6)": "Upload objects in an S3 bucket",
      "7)": "Delete objects from an S3 bucket",
      "8)": "Return to the main menu"
  }

  while True:

    for key, value in menu_s3.items():
      print(f"{key} {value}")

    ask_option = input("\nPlease select the operation you "\
                       "want to execute on the EC2 service: ")
    
    if ask_option == "1":
      sns_flag = s3_class.s3_file_distribution()
      if sns_flag[0] == "yes":
        print("\nThe distribution has been completed and the mail sent")
        sns_class.sns_post()
        next_option()
        
    elif ask_option == "2":
      s3_class.s3_creation()
      next_option()
    
    elif ask_option == "3":
      s3_class.delete_s3()
      next_option()

    elif ask_option == "4":
      s3_class.list_buckets_s3()
      next_option()
      
    elif ask_option == "5":
      s3_class.object_list_s3()
      next_option()
      
    elif ask_option == "6":
      s3_class.upload_obj_s3()
      next_option()
      
    elif ask_option == "7":
      s3_class.delete_obj_s3()
      next_option()
      
    elif ask_option == "8":
      print("Returning to the main menu...")
      time.sleep(1)
      os.system('clear')
      break
      
    else:
      print("Invalid option!") 
      time.sleep(1)
      os.system('clear')


def main_menu():

  options = ['1', '2', '3']
  main_menu = {
      "1)": "Show EC2 operations",
      "2)": "Show S3 operations",
      "3)": "Show DynamoDB operations",
      "4)": "Quit program"
  }

  for key, value in main_menu.items():
    print(f"{key} {value}")

  ask_option = input("\nPlease select the service you want to use: ")

  if ask_option in options and ask_option != "4":
    return ask_option
    
  elif ask_option not in options and ask_option != "4":
    print("Invalid option!") 
    time.sleep(1)
    os.system('clear')
    
  elif ask_option == '4':
    os.system('clear')
    print("Closing session with AWS services...")
    time.sleep(1)
    print("Session closed!")
    quit()
    
  else:
    print("Please introduce a valid option")
