import os
from dotenv import load_dotenv
import psycopg2
from werkzeug.security import check_password_hash
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
        connection = self.get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        print(user)

        cursor.close()
        connection.close()

         # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user:
            return {"statusCode": response_codes["INTERNAL_ERROR"], "message": "User not found"}
        elif user[6] != password:
            return {"statusCode": response_codes["INTERNAL_ERROR"], "message": "Invalid credentials"}
        else:
            response = {
                "statuCode": response_codes["SUCCESS"],
                "message": "Login successful",
                'data': {
                    "first_name":user.first_name,
                    "last_name":user.last_name,
                    "age": user.age,
                    "email": user.email,
                    "phone": user.phone,
                },
            }
            return response
    
        
