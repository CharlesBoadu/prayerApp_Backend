import os
from dotenv import load_dotenv
import bcrypt
import psycopg2
from app.config import response_codes
from app.libs.email import send_invite_user_mail
from app.libs.paswordGenerator import passwordGenerator
from app.libs.utils import Utilities
import flask_bcrypt
from app.libs.email import send_reset_password_email


# Load environment variables from .env file
load_dotenv()

class LoginService:
    def get_db_connection(self):
        """
        name: get_db_connection
        params: null
        description: connect to postgresql db using psycopg2
        dependencies:psycopg2
        references:
        """
        conn = psycopg2.connect(host='localhost',
                                database='prayer_app',
                                user=os.getenv('DB_USERNAME'),
                                password=os.getenv('DB_PASSWORD'))
        return conn
    
    def authenticate_user(self,request): 
        """
            name: authenticate_user
            params: request
            description: verify credentials
            dependencies:psycopg2
            references:
        """

        data = request.json
        email = data.get('email')
        password = data.get('password')

        #Establishing a connection to the database
        connection = self.get_db_connection()
        cursor = connection.cursor()


        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
 
        cursor.close()
        connection.close()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user:
            return {"statusCode": response_codes["NOT_FOUND"], "message": "User not found"}
        elif email == "" or password == "":
            return {"statusCode": response_codes["INTERNAL_ERROR"], "message": "Email or password cannot be empty"}
        else: 
            if not bcrypt.checkpw(password.encode('utf-8'), user[9].encode('utf-8')):
                return {"statusCode": response_codes["INTERNAL_ERROR"], "message": "Password is incorrect"}           
            response = {
                "statusCode": response_codes["SUCCESS"],
                "message": "Login successful",
                'data': {
                    "id": user[0],
                    "first_name":user[1],
                    "last_name":user[2],
                    "age": user[4],
                    "email": user[3],
                    "phone": user[5],
                    "role": user[6],
                    "organization": user[7],
                    "organization_id": user[8]
                },
            }
            return response

class RegisterService:
    def get_db_connection(self):
        """
        name: get_db_connection
        params: null
        description: connect to postgresql db using psycopg2
        dependencies:psycopg2
        references:
        """
        conn = psycopg2.connect(host='localhost',
                                database='prayer_app',
                                user=os.getenv('DB_USERNAME'),
                                password=os.getenv('DB_PASSWORD'))
        return conn 
    
    def register_user(self,request): 
        """
            name: register_user
            params: request
            description: verify credentials
            dependencies:psycopg2
            references:
        """

        data = request.json
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        age = data.get('age')
        phone = data.get('phone')
        role = data.get('role')
        password = data.get('password')
        organization = data.get('organization')
        connection = self.get_db_connection()
        organization_id = Utilities().gen_id()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            return {"statusCode": response_codes["ALREADY_EXIST"], "message": "User already exists"}
        elif first_name == "" or last_name == "" or age == "" or email == "" or phone == "" or role == "":
            return {"statusCode": response_codes["INTERNAL_ERROR"], "message": "fields cannot be empty"}
        elif len(phone) < 10 or len(phone) > 10:
            return {"statusCode": response_codes["INTERNAL_ERROR"], "message": "phone number should be 10 digits"}
        else:
            hashed_pw = flask_bcrypt.generate_password_hash(password).decode('utf8')
            cursor.execute('INSERT INTO users (first_name, last_name, email, age, phone, role, password, organization, organization_id)'
                        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (first_name,
                        last_name,
                        email,
                        age,
                        phone,
                        role,
                        hashed_pw,
                        organization,
                        organization_id)
                        
                        )
            connection.commit()
            cursor.close()
            connection.close()

            response = {
                "statusCode": response_codes["SUCCESS"],
                "message": "User registered successfully",
                'data': {
                    "first_name":first_name,
                    "last_name":last_name,
                    "email": email,
                    "age": age,
                    "phone": phone,
                    "role": role,
                    "organization": organization,
                    "organization_id": organization_id
                },
            }
            return response
        
    def register_user_by_admin(self,request): 
        """
            name: register_user_by_admin
            params: request
            description: Adding a new user by an Admin
            dependencies:psycopg2
            references:
        """

        data = request.json
        organization_id = data.get('organization_id')
        organization = data.get('organization')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        age = data.get('age')
        phone = data.get('phone')
        role = data.get('role')
        password = passwordGenerator(10)
        connection = self.get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s AND organization_id = %s", (email, organization_id))
        user = cursor.fetchone()
        cursor.execute("SELECT * FROM users WHERE organization = %s AND organization_id = %s", (organization, organization_id,))
        org = cursor.fetchone()

        if user:
            return {"statusCode": response_codes["ALREADY_EXIST"], "message": "User already exists"}
        elif not org:
            return {"statusCode": response_codes["INTERNAL_ERROR"], "message": "Organization does not exist"}
        elif first_name == "" or last_name == "" or age == "" or email == "" or phone == "" or role == "" or organization_id == "":
            return {"statusCode": response_codes["INTERNAL_ERROR"], "message": "fields cannot be empty"}
        elif len(phone) < 10 or len(phone) > 10:
            return {"statusCode": response_codes["INTERNAL_ERROR"], "message": "phone number should be 10 digits"}
        else:
            hashed_pw = flask_bcrypt.generate_password_hash(password).decode('utf8')
            cursor.execute('INSERT INTO users (first_name, last_name, email, age, phone, role, password, organization, organization_id)'
                        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (first_name,
                        last_name,
                        email,
                        age,
                        phone,
                        role,
                        hashed_pw,
                        organization,
                        organization_id)
                        )
            connection.commit()
            
            send_invite_user_mail(email, first_name, last_name, password)

            cursor.close()
            connection.close()

            response = {
                "statusCode": response_codes["SUCCESS"],
                "message": "User Added successfully by Admin",
                'data': {
                    "first_name":first_name,
                    "last_name":last_name,
                    "email": email,
                    "age": age,
                    "phone": phone,
                    "role": role,
                    "organization": organization,
                },
            }
            return response
        
class ResetPasswordService:
    def get_db_connection(self):
        """
        name: get_db_connection
        params: null
        description: connect to postgresql db using psycopg2
        dependencies:psycopg2
        references:
        """
        conn = psycopg2.connect(host='localhost',
                                database='prayer_app',
                                user=os.getenv('DB_USERNAME'),
                                password=os.getenv('DB_PASSWORD'))
        return conn
    
    def send_reset_password(self,request):
        """
            name: reset_password
            params: request
            description: reset user password
            dependencies:psycopg2
            references:
        """
        data = request.json
        email = data.get('email')
        
        #Establishing a connection to the database
        connection = self.get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            return {"statusCode": response_codes["NOT_FOUND"], "message": "User not found"}
        else: 
            # hash the password
            temp_password = passwordGenerator(10)
        
            cursor.execute("UPDATE users SET temp_password = %s WHERE email = %s", (temp_password, email))
            connection.commit()

            send_reset_password_email(email, user[1], temp_password)
            
            cursor.close()
            connection.close()
            
            response = {
                "statusCode": response_codes["SUCCESS"],
                "message": "Reset Password Email Sent Successfully"
            }
            return response
        
    def reset_password(self,request):
        """
            name: reset_password
            params: request
            description: reset user password
            dependencies:psycopg2
            references:
        """
        data = request.json
        email = data.get('email')
        temp_password = data.get('temp_password')
        new_password = data.get('new_password')
        
        #Establishing a connection to the database
        connection = self.get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            return {"statusCode": response_codes["NOT_FOUND"], "message": "User not found"}
        else: 
            if user[8] != temp_password:
                return {"statusCode": response_codes["INTERNAL_ERROR"], "message": "Invalid temp password"}
            
            hashed_pw = flask_bcrypt.generate_password_hash(new_password).decode('utf8')
            cursor.execute("UPDATE users SET password = %s, temp_password = %s WHERE email = %s", (hashed_pw, None, email))
            connection.commit()
            
            cursor.close()
            connection.close()
            
            response = {
                "statusCode": response_codes["SUCCESS"],
                "message": "Password Reset Successfully"
            }
            return response
        

class UpdatePasswordService:
    def get_db_connection(self):
        """
        name: get_db_connection
        params: null
        description: connect to postgresql db using psycopg2
        dependencies:psycopg2
        references:
        """
        conn = psycopg2.connect(host='localhost',
                                database='prayer_app',
                                user=os.getenv('DB_USERNAME'),
                                password=os.getenv('DB_PASSWORD'))
        return conn 
    
    def update_password(self,request,id): 
        """
            name: update_password
            params: request
            description: verify credentials
            dependencies:psycopg2
            references:
        """

        data = request.json
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        connection = self.get_db_connection()
        cursor = connection.cursor()


        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        user = cursor.fetchone()

        if not user:
            return {"statusCode": response_codes["NOT_FOUND"], "message": "User not found"}
        elif old_password == "" or new_password == "" or confirm_password == "":
            return {"statusCode": response_codes["INTERNAL_ERROR"], "message": "fields cannot be empty"}
        else:
            if not bcrypt.checkpw(old_password.encode('utf-8'), user[6].encode('utf-8')):
                return {"statusCode": response_codes["INTERNAL_ERROR"], "message": "Incorrect old password"}
            elif new_password != confirm_password:
                return {"statusCode": response_codes["INTERNAL_ERROR"], "message": "New password and Confirm password do not match"}
            else:
                hashed_new_pw = flask_bcrypt.generate_password_hash(new_password).decode('utf8')
                cursor.execute('UPDATE users SET password = %s WHERE id = %s',
                           (hashed_new_pw,
                        id))
                connection.commit()
                cursor.close()
                connection.close()
                response = {
                    "statusCode": response_codes["SUCCESS"],
                    "message": "User Password updated successfully",
                }
                return response