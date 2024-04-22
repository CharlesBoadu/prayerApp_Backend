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
    
    def get_user(self,request): 
        """
            name: get_user
            params: request
            description: get user by id
            dependencies:psycopg2
            references:
        """
        connection = self.get_db_connection()
        cursor = connection.cursor()
        data = request.json
        user_id = data.get('user_id')
        organization_id = data.get('organization_id')
        
        cursor.execute("SELECT * FROM users WHERE id = %s AND organization_id = %s", (user_id, organization_id))
        user = cursor.fetchone()

        if user:
            response = {
                "statusCode": response_codes["SUCCESS"],
                "message": "User retrieved successfully",
                'data': {
                    "id": user[0],
                    "first_name": user[1],
                    "last_name": user[2],
                    "email": user[3],
                    "age": user[4],
                    "phone": user[5],
                    "role": user[6],
                    "organization": user[7],
                }
            }
            return response
        else:
            return {"statusCode": response_codes["NOT_FOUND"], "message": "User does not exist"}
        
    def get_users_by_organization(self,request): 
        """
            name: get_users_by_organization
            params: request
            description: get users by Organization using Organization ID
            dependencies:psycopg2
            references:
        """
        connection = self.get_db_connection()
        cursor = connection.cursor()

        data = request.json
        organization_id = data.get('organization_id')
        

        cursor.execute("SELECT * FROM users WHERE organization_id = %s", (organization_id,))
        users = cursor.fetchall()
        if users:
            response = {
                "statusCode": response_codes["SUCCESS"],
                "message": "User retrieved successfully",
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
        else:
            return {"statusCode": response_codes["NOT_FOUND"], "message": "Organization Does not Exist"}
        
    def delete_user(self,request,id):
        """
            name: delete_user
            params: request
            description: delete user by id
            dependencies:psycopg2
            references:
        """
        connection = self.get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        user = cursor.fetchone()
        if user:
            cursor.execute("DELETE FROM users WHERE id = %s", (id,))
            connection.commit()
            return {"statusCode": response_codes["SUCCESS"], "message": "User deleted successfully"}
        else:
            return {"statusCode": response_codes["NOT_FOUND"], "message": "User does not exist"}
        
    def update_user(self,request,id):
        """
            name: update_user
            params: request
            description: update user by id
            dependencies:psycopg2
            references:
        """
        connection = self.get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        user = cursor.fetchone()

        data = request.json
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        age = data.get('age')
        phone = data.get('phone')
        role = data.get('role')

        if user:
            cursor.execute('UPDATE users SET first_name = %s, last_name = %s, email = %s, age = %s, phone = %s, role = %s WHERE id = %s',
                        (first_name,
                        last_name,
                        email,
                        age,
                        phone,
                        role,
                        id)
                        )
            connection.commit()
            return {"statusCode": response_codes["SUCCESS"], "message": "User updated successfully"}
        else:
            return {"statusCode": response_codes["NOT_FOUND"], "message": "User does not exist"}