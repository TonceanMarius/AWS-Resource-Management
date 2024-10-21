from menu import dynamodb_menu, ec2_menu, s3_menu, main_menu
import os 

if __name__ == "__main__":

  while True:
  
    options = main_menu()
  
    if options == "1":
      os.system('clear')
      ec2_menu()
      
    elif options == "2":
      os.system('clear')
      s3_menu()
      
    elif options == "3":
      os.system('clear')
      dynamodb_menu()  