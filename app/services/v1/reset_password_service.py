import os
from dotenv import load_dotenv
import flask_bcrypt
import psycopg2
from app.config import response_codes
from app.libs.paswordGenerator import passwordGenerator
from app.libs.email import send_reset_password_email

# Load environment variables from .env file
load_dotenv()

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
            return {"statusCode": response_codes["USER_NOT_FOUND"], "message": "User not found"}
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
            return {"statusCode": response_codes["USER_NOT_FOUND"], "message": "User not found"}
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