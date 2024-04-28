import os
from dotenv import load_dotenv
import psycopg2
from app.config import response_codes


# Load environment variables from .env file
load_dotenv()

class UpdateProfileService:
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
    
    def update_profile(self,request,id): 
        """
            name: update_profile
            params: request
            description: update user profile
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


        if user:
            cursor.execute('UPDATE users SET first_name = %s, last_name = %s, age = %s, phone = %s, email = %s WHERE id = %s',
                        (first_name,
                        last_name,
                        age,
                        phone,
                        email,
                        id)
                        )
            connection.commit()
            cursor.close()
            connection.close()
            return {"statusCode": response_codes["SUCCESS"], "message": "Profile updated successfully"}
        else:
            return {"statusCode": response_codes["NOT_FOUND"], "message": "User does not exist"}