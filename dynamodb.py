import os
import boto3
from other_functions import aws_setup_config
from boto3.dynamodb.conditions import Key, Attr

class DynamoDB_Operations():

  def __init__(self):
    self.session = aws_setup_config()
    self.dynamodb_resource = self.session.resource('dynamodb', region_name=os.getenv('AWS_REGION'))
    self.dynamodb_client = self.session.client('dynamodb', region_name=os.getenv('AWS_REGION'))

  def dynamodb_create(self):

    ask_db = input("\nPlease specify the name of the DynamoDB you want to create or q to quit: ")
    if ask_db != 'q':
      print("The DynamoDB is currently creating, please wait...")
      table = self.dynamodb_resource.create_table(
        TableName = ask_db,
        KeySchema = [
          {
            'AttributeName': 'username',
            'KeyType' : 'HASH'
          },
        ],
        AttributeDefinitions=[
          {
            'AttributeName': 'username',
            'AttributeType': 'S'
          },
        ],
        ProvisionedThroughput={
          'ReadCapacityUnits': 5,
          'WriteCapacityUnits': 5
        }
      )
  
      table.wait_until_exists()
      print(f'\nThe table {ask_db} has been successfully created!')
    else:
      return

  def dynamodb_list(self):

    db_list = []
    print("\nHere is the list of tables in the DynamoDB:")
    response = self.dynamodb_client.list_tables()
    for table in response['TableNames']:
      db_list.append(table)
      print(table)

    return db_list
  
  def dynamodb_delete(self):

    db_list=self.dynamodb_list()
    while True:
      ask_db = input("\nPlease specify the table that you want to delete or q to quit: ")
      if ask_db != 'q':
        if ask_db in db_list:
          print('The DynamoDB table is currently deleting, please wait...')
          try:
            self.dynamodb_client.delete_table(TableName = ask_db)
            waiter = self.dynamodb_client.get_waiter('table_not_exists')
            waiter.wait(TableName=ask_db)
            print(f"\nThe table {ask_db} has been successfully deleted")
          except Exception:
            print(f"\nThere is an error with the deletion of the table {ask_db}")
          break
        else:
          print("\nThe table doesn't exist!")
      else:
        return

  def insert_item(self):

    while True:
      db_list = self.dynamodb_list()
      ask_db = input("\nPlease specify the table that you want to place items or q to quit: ")
      if ask_db != 'q':
        if ask_db in db_list:
          table =self.dynamodb_resource.Table(ask_db)
          ask_nr = int(input("\nHow many non zero items do you want in the table? "))
          if ask_nr == 0:
            print("\nNumber must be bigger than 0")
            continue
          else:
            with table.batch_writer(overwrite_by_pkeys=['username']) as batch:
              for number in range(ask_nr):
                ask_username = input(f"\nSpecify the username for"\
                                     f" entry number {number+1}: ")
                ask_first_name = input(f"Specify the first name for "\
                                       f" the entry number {number+1}: ")
                ask_last_name = input(f"Specify the last name for "\
                                      f" the entry number {number+1}: ")
                ask_age = input(f"Specify the age for "\
                                f" the entry number {number+1}: ")
                ask_acc_type = input(f"Specify the account type for "\
                                     f" the entry number {number+1}: ")
                batch.put_item(
                    Item={
                      'username': ask_username,
                      'first_name': ask_first_name,
                      'last_name': ask_last_name,
                      'age': ask_age,
                      'account_type': ask_acc_type
                    }
                )
            print("\nThe items have been successfully added\n")
            break
        else:
          print("\nThe table doesn't exist!")
          while True:
            ask = input("\nDo you want to create a table? (y/n) ")
            if ask == "y":
              self.dynamodb_create()
              break
            elif ask == "n":
              break
            else:
              print("\nInvalid option!")
              print("\nReturning to the main menu...")
              break
      else:
        return

  def check_table_items(self):

    db_list = self.dynamodb_list()
    ask_table = input(
      "\nPlease introduce the name for the table you want its items: "
    )
    while True:
      if ask_table in db_list:
        table = self.dynamodb_resource.Table(ask_table)
        response = table.scan()
        items = response['Items']
        if items:
          print(f"\nThe items present in the table {ask_table} are: \n")
          for item in items:
            print(f"\nusername : {item['username']}\nfirst name : {item['first_name']}\n"\
                  f"last name : {item['last_name']}\nage : {item['age']}\n"\
                  f"account_type : {item['account_type']}\n")
          break
        else:
          print('\nTable is empty')
          return "empty"
      else:
        print("\nThe table doesn't exist!")
        break
      

  def delete_items(self):

    # Get the list of DynamoDB tables and display them once
    db_list = self.dynamodb_list()

    while True:
        ask_table = input("\nPlease specify the table you want to delete content from or 'q' to quit: ").strip()

        if ask_table == 'q':
            return

        # Check if the specified table is in the list of DynamoDB tables
        if ask_table in db_list:
            # Set the table for further operations
            self.current_table = ask_table  # Assuming you use current_table in check_table_items

            # Check if the table contains any items directly
            #if self.check_table_items() != "empty":
            while True:
              if ask_table in db_list:
                table = self.dynamodb_resource.Table(ask_table)
                response = table.scan()
                items = response['Items']
                if items:
                  print(f"\nThe items present in the table {ask_table} are:")
                  for item in items:
                    print(f"\nusername : {item['username']}\nfirst name : {item['first_name']}\n"\
                          f"last name : {item['last_name']}\nage : {item['age']}\n"\
                          f"account_type : {item['account_type']}\n")
                    
                  ask_delete = input("\nSpecify the item you want to delete by its username: ").strip()

                  table.delete_item(
                    Key={'username': ask_delete}
                  )
                  print(f"\nThe item '{ask_delete}' has been successfully deleted!")

                  # Ask if the user wants to delete more items
                  ask_all = input("\nIs that all? (y/n): ").strip().lower()
                  if ask_all == 'y':
                    return  # Exit the loop and end the function
                  elif ask_all == 'n':
                    pass  # Continue to delete more items
                  else:
                    print("\nInvalid option. Please choose 'y' or 'n'.")
                  break
                else:
                  print('\nTable is empty')
                  return "empty"
            #       table = self.dynamodb_resource.Table(ask_table)

            #     while True:
            #         ask_delete = input("\nSpecify the item you want to delete by its username: ").strip()

            #         # Perform the delete operation
            #         table.delete_item(
            #             Key={'username': ask_delete}
            #         )
            #         print(f"\nThe item '{ask_delete}' has been successfully deleted!")

            #         # Ask if the user wants to delete more items
            #         ask_all = input("\nIs that all? (y/n): ").strip().lower()
            #         if ask_all == 'y':
            #             return  # Exit the loop and end the function
            #         elif ask_all == 'n':
            #             pass  # Continue to delete more items
            #         else:
            #             print("\nInvalid option. Please choose 'y' or 'n'.")
            # else:
            #     print(f"\nThe table '{ask_table}' is empty, nothing to delete.")
            #     return
        else:
            print("\nThe specified table does not exist. Please try again.")


