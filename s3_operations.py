import time
import os
from botocore.exceptions import ClientError
from other_functions import aws_setup_config

class S3Operations:

  def __init__(self):
    self.session = aws_setup_config()
    self.s3_resource = self.session.resource('s3')
    self.s3_client = self.session.client('s3')
  
  def s3_file_distribution(self):

    bucket = self.s3_resource.Bucket("dct-sales123")
    lista = []
    destination_name = ["sr1", "sr2", "sr3", "sr4", "sr5"] 
    for index, obj in enumerate(bucket.objects.all()):
      key_parts = obj.key.split("/")
      if index == 0 or key_parts[0] in destination_name:
        continue
      else:
        lista.append(obj.key)
        if obj.key.endswith(".csv"):
          copy_source = {'Bucket': "dct-sales123", 'Key': obj.key}
          ind = destination_name.index(key_parts[1].split("_")[0])
          final = f"{destination_name[ind]}/{key_parts[1]}"
          bucket.copy(copy_source, final)

    return "yes", lista


  def s3_creation(self):

    location_list = ['eu-central-1','eu-west-1','eu-west-2','eu-central']
    bucket_name = input("\nIntroduce the name of the new S3 bucket or 'q' to quit: ")
    if bucket_name != 'q':
      location = input(f"\nIntroduce the location of the new S3 bucket from the list:\n"\
                       f"{', '.join(location_list)}: ")
  
      if location in location_list:
        try:
          self.s3_client.create_bucket(
              ACL='private',
              Bucket=bucket_name,
              CreateBucketConfiguration={
                  'LocationConstraint': location,
              },
          )
          print("\nS3 bucket created successfully")
        except ClientError:
          print("\nThe bucket already exists")
          
      else:
        print("\nInvalid location")
    else:
      pass

  def list_buckets_s3(self):

    bucket_list = []
    
    try:
      response = self.s3_client.list_buckets(MaxBuckets=123, ContinuationToken='string')
      print("\nThe available buckets are: \n")
      for resp in response['Buckets']:
        bucket_list.append(resp['Name'])
        print(f"{resp['Name']}")
    except ClientError as e:
      print(f"An error occurred: {e}")
    
    return bucket_list
  
  def object_list_s3(self):

    list_buckets = self.list_buckets_s3()

    if not list_buckets:
        print("No buckets found")
        return "nothing"

    # Prompt the user to select a bucket or quit
    ask = input("\nPlease select the bucket you want to show or delete objects from, or type 'q' to quit: ").strip()

    # Check if the user wants to quit
    if ask.lower() == 'q':
        return 'quit'

    # Check if the chosen bucket exists in the bucket list
    if ask not in list_buckets:
        print(f"\nThe bucket '{ask}' doesn't exist. Please check the name and try again.")
        return "nothing"

    try:
        # List objects in the selected bucket
        response = self.s3_client.list_objects_v2(Bucket=ask, MaxKeys=123)

        # Check if the bucket has any objects
        if 'Contents' in response:
            print(f"\nThe objects in the bucket '{ask}' are:\n")
            list_obj = [obj['Key'] for obj in response['Contents']]
            for obj_key in list_obj:
                print(f" * {obj_key}")
            return list_obj, ask, response['KeyCount']
        else:
            print(f"\nThe bucket '{ask}' is empty.")
            return ask

    except self.s3_client.exceptions.NoSuchBucket:
        print(f"\nThe bucket '{ask}' does not exist.")
        return "nothing"
    except Exception as e:
        print(f"\nAn error occurred while listing objects from the bucket '{ask}': {e}")
        return "nothing"


  def delete_obj_s3(self):
    """
    Handles object deletion from an S3 bucket based on user input.
    The function allows the user to delete all or specific objects from a selected bucket.
    """

    # Retrieve the object list from the bucket
    list_obj = self.object_list_s3()

    # Check if there are valid objects to delete
    if list_obj != "nothing" and list_obj != "quit":
        bucket = list_obj[1]  # The selected bucket

        # Ensure list_obj[2] is an integer
        try:
            object_count = int(list_obj[2])  # Convert to int if possible
        except Exception:
          return

        obj_delete = [{'Key': key} for key in list_obj[0]]  # List of objects to delete

        while True:
            # Check if there are objects in the bucket
            if object_count != 0:
                print(f"\nThe bucket '{bucket}' contains {object_count} object(s).")
                ask_option = input(
                    f"\nDo you wish to delete all objects from the bucket '{bucket}'? (y/n): "
                ).strip().lower()

                if ask_option == 'n':
                    number = input("\nPlease specify how many objects you want to delete or 'q' to quit: ").strip()

                    if number.isdigit():
                        number = int(number)
                        if 0 < number <= object_count:  # Safely compare numbers
                            for _ in range(number):
                                obj = input("\nPlease enter the object key you want to delete: ").strip()
                                for o in obj_delete:
                                    if o['Key'] == obj:
                                        self.s3_client.delete_objects(
                                            Bucket=bucket,
                                            Delete={
                                                'Objects': [o],
                                                'Quiet': True
                                            }
                                        )
                                        print(f"\nThe object '{o['Key']}' from the bucket '{bucket}' has been successfully deleted!")
                                        break
                            break  # Exit the loop after deleting specified objects
                        else:
                            print(f"\nPlease enter a number between 1 and {object_count}.")
                            continue  # Re-prompt the user for input
                    elif number == "q":
                        print("\nOperation canceled by the user.")
                        break  # Exit the loop
                    else:
                        print("\nPlease enter a valid number or 'q' to quit.")
                        continue  # Re-prompt the user

                elif ask_option == "y":
                    self.s3_client.delete_objects(
                        Bucket=bucket,
                        Delete={
                            'Objects': obj_delete,
                            'Quiet': True
                        }
                    )
                    print(f"\nAll objects from the bucket '{bucket}' have been successfully deleted!")
                    break  # Exit the loop
                else:
                    print("\nInvalid option. Please choose 'y' or 'n'.")
                    continue  # Re-prompt the user
            else:
                print(f"\nThe bucket '{bucket}' is already empty!")
                break  # Exit the loop if the bucket is empty


  def upload_obj_s3(self):

    list_bucket = self.list_buckets_s3()
    list_files = ['test1.txt', 'test2.txt', 'test3.txt']
    
    print("\nThis is the list of files that can be uploaded in the bucket:\n ")
    if list_bucket:
      for f in list_files:
        print(f)
      while True:
        ask_s3 = input(
            "\nPlease select the bucket that you want to upload objects to: ")
        if ask_s3 in list_bucket:
          while list_files:
            
            ask_file = input(f'\nPlease introduce the name of the file that'
                             f' you want to upload in the bucket {ask_s3}'
                             f' or "q" to quit: ')
            if ask_file in list_files:
              self.s3_client.upload_file(ask_file, ask_s3, ask_file)
              list_files.remove(ask_file)
              print(f"\nThe file {ask_file} has been successfully"\
                    f" added to the bucket {ask_s3} ")
            elif ask_file == "q":
              break
              
            else:
              print("\nElement doesn't exist in the list")
          print(f"\nAll the files have been added in the bucket {ask_s3} ")
          break
        else:
          print(f"\nThe bucket {ask_s3} doens't exist")


  def delete_s3(self):

    result = self.object_list_s3()

    # Check the return value from object_list_s3
    if isinstance(result, tuple):  # This means the bucket has objects (non-empty)
        list_obj, bucket_name, key_count = result
        print(f"\nThe bucket '{bucket_name}' contains {key_count} object(s).\n")
        print("Bucket must be emptied first")

    elif result == "nothing" or result == 'quit':
      pass

    elif isinstance(result, str) and result != "quit":  # This means the bucket is empty
        bucket_name = result

        self.s3_client.delete_bucket(Bucket=bucket_name)
        print(f"\nBucket '{bucket_name}' has been deleted successfully.")
    
    
    