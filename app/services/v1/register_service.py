import os
from dotenv import load_dotenv
import flask_bcrypt
import psycopg2
from app.config import response_codes

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
        password = data.get('password')
        connection = self.get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            return {"statusCode": response_codes["ALREADY_EXIST"], "message": "User already exists"}
        elif first_name == "" or last_name == "" or age == "" or email == "" or password == "":
            return {"statusCode": response_codes["INTERNAL_ERROR"], "message": "fields cannot be empty"}
        elif len(phone) < 10 or len(phone) > 10:
            return {"statusCode": response_codes["INTERNAL_ERROR"], "message": "phone number should be 10 digits"}
        else:
            hashed_pw = flask_bcrypt.generate_password_hash(password).decode('utf8')
            cursor.execute('INSERT INTO users (first_name, last_name, email, age, phone, password)'
                        'VALUES (%s, %s, %s, %s, %s, %s)',
                        (first_name,
                        last_name,
                        email,
                        age,
                        phone,
                        hashed_pw)
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
                    "age": age,
                    "email": email,
                    "phone": phone,
                },
            }
            return response


    
        
