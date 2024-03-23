import os
from dotenv import load_dotenv
import bcrypt
import psycopg2
from app.config import response_codes

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
            return {"statusCode": response_codes["USER_NOT_FOUND"], "message": "User not found"}
        elif email == "" or password == "":
            return {"statusCode": response_codes["INTERNAL_ERROR"], "message": "Email or password cannot be empty"}
        else: 
            if not bcrypt.checkpw(password.encode('utf-8'), user[7].encode('utf-8')):
                return {"statusCode": response_codes["INTERNAL_ERROR"], "message": "Password is incorrect"}           
            response = {
                "statusCode": response_codes["SUCCESS"],
                "message": "Login successful",
                'data': {
                    "id": user[0],
                    "first_name":user[1],
                    "last_name":user[2],
                    "age": user[3],
                    "email": user[4],
                    "phone": user[5],
                },
            }
            return response
    
        
