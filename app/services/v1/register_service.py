import os
from dotenv import load_dotenv
import flask_bcrypt
import psycopg2
from app.config import response_codes
from app.libs.utils import Utilities
from app.libs.email import send_invite_user_mail
from app.libs.paswordGenerator import passwordGenerator

# Load environment variables from .env file
load_dotenv()

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

        
