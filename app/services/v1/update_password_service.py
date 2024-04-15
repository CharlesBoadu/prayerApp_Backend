import os
from dotenv import load_dotenv
import bcrypt
import flask_bcrypt
import psycopg2
from app.config import response_codes

# Load environment variables from .env file
load_dotenv()

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


    
        
