import os
from dotenv import load_dotenv
import psycopg2
from app.config import response_codes


# Load environment variables from .env file
load_dotenv()

class UsersService:
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
    
    def get_users(self,request): 
        """
            name: get_users
            params: request
            description: get all users
            dependencies:psycopg2
            references:
        """
        connection = self.get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        response = {
                        "statusCode": response_codes["SUCCESS"],
                        "message": "Users retrieved successfully",
                        'data': [
                            {
                                "id": user[0],
                                "first_name": user[1],
                                "last_name": user[2],
                                "email": user[3],
                                "age": user[4],
                                "phone": user[5],
                                "role": user[6],
                            } for user in users
                        ],
                    }

        return response