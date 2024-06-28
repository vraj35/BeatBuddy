import mysql.connector
from datetime import datetime

# import playlist_backup as backup
import random
import os
import shutil 


class authentication:
    email_id = None

    def __init__(self):
        self.con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="beatbuddy",
            autocommit=True,
        )
        self.mycursor = self.con.cursor()
        # self.backup_obj = backup.Playlist_backup()

    def login(self):
        while True:
            print(
                """
1. login via phone no.
2. login via Email-id
3. login via User-id
4. Back
5. Exit"""
            )
            choice = None
            while not choice:
                choice = input("Enter you choice : ")
            choice = int(choice)
            match (choice):
                case 1:
                    while True:
                        phone_no = data = input("Enter your phone number : ")
                        if phone_no.isdigit():
                            if len(phone_no) == 10:
                                if self.check_existancy("phone_no", phone_no) == True:
                                    self.fatch_email_id("phone_no", phone_no)
                                    break
                                else:
                                    print("This phone no. is not registered")
                            else:
                                print(
                                    "Invalid phone number format. Please enter a 10-digit phone number."
                                )
                        else:
                            print("phone number contains only digits")
                    column_name = "phone_no"
                    break
                case 2:
                    while True:
                        self.email_id = data = input("Enter your Email-id : ")
                        if self.check_existancy("email_id", self.email_id) == True:
                            break
                        else:
                            print("This Email-id is not registered")
                    column_name = "email_id"
                    break
                case 3:
                    while True:
                        user_id = data = input("Enter your User-id : ")
                        if self.check_existancy("user_id", user_id) == True:
                            self.fatch_email_id("user_id", user_id)
                            break
                        else:
                            print("This User-id is not registered")
                    column_name = "user_id"
                    break
                case 4:
                    pass
                case 5:
                    exit()
                case _:
                    print("!! Enter valid choice")
        while True:
            query = "Select password from user_details where " + column_name + " = %s"
            val = (data,)
            self.mycursor.execute(query, val)
            actual_password = self.mycursor.fetchone()[0]
            ip_password = input("Enter password : ")
            if actual_password == ip_password:
                print("------------ Login succesful -------------")
                break
            else:
                print("!! Wrong password .Please enter valid password")
                print("----------------------------------------")
                print("1. Want to forgot password ?")
                print("2. Try again")
                print("3. Exit")
                choice = int(input("Ener choice = "))
                if choice == 1:
                    self.forgotpassword()
                elif choice == 2:
                    continue
                elif choice == 3:
                    exit()
                else:
                    print("** Enter valid choice **")

    def fatch_email_id(self, column_name, data):
        query = "Select email_id from user_details where " + column_name + " = %s"
        val = (data,)
        self.mycursor.execute(query, val)
        self.email_id = self.mycursor.fetchone()[0]

    def check_existancy(self, column_name, data):
        query = "Select count(*) from user_details where " + column_name + " = %s"
        val = (data,)
        self.mycursor.execute(query, val)
        count = self.mycursor.fetchone()[0]
        if count == 1:
            return True
        else:
            return False

    def signup(self):
        self.email_id = input("Enter email id : ")
        phone_no = input("Enter phone no : ")
        birth_date = input("Enter birthdate (format : yyyy-mm-dd) : ")
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()  # used for parsing strings representing dates and times into datetime objects. It stands for "string parse time."
        user_id = input("Enter user-id : ")
        password = input("Enter password : ")
        query = "INSERT INTO user_details(user_id,phone_no,email_id,password,birth_date) values(%s,%s,%s,%s,%s)"
        val = (user_id, phone_no, self.email_id, password, birth_date)
        self.mycursor.execute(query, val)
        # os.mkdir("D:\\beatbuddy")
        print("Account successfully registered")
        if os.path.exists("D:\\beatbuddy"):
            shutil.rmtree("D:\\beatbuddy") #delete folder method
        os.mkdir("D:\\beatbuddy")
        folder_path = "D:\\beatbuddy"
        shutil.make_archive("beatbuddy", "zip", folder_path) #zip file to upload in database
        f = open("beatbuddy.zip", "rb") #readbytes- byte ma read kre-to store in db as bytes have been stored 
        data = f.read()
        f.close()
        os.remove("beatbuddy.zip")
        query = "INSERT INTO backup(email_id,data) values(%s,%s)"
        val = (self.email_id, data)
        self.mycursor.execute(query, val)
        print()

    def forgotpassword(self):
        genrated_otp = random.randint(100000, 999999)
        print("OTP is :", genrated_otp)
        otp = int(input("Enter OTP : "))
        if genrated_otp == otp:
            password = input("Enter new password : ")
            query = "Update user_details set password = %s where email_id=%s"
            val = (password, self.email_id)
            self.mycursor.execute(query, val)
            print("password succesfully changed")
        else:
            print("Wrong OTP")
            self.forgotpassword()
