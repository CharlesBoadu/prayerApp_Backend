import os
from dotenv import load_dotenv
import psycopg2
from app.config import response_codes

# Load environment variables from .env file
load_dotenv()

class PrayerService:
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
    
    def add_prayer(self,request): 
        """
            name: add_prayer
            params: request
            description: verify credentials
            dependencies:psycopg2
            references:
        """

        data = request.json
        prayer = data.get('prayer')
        scripture = data.get('scripture')
        category = data.get('category')
        user_id = data.get('user_id')

        #Establishing a connection to the database
        connection = self.get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if prayer == "" or scripture == "" or category == "" or user_id == "":
            return {"statusCode": response_codes["INTERNAL_ERROR"], "message": "Prayer, category or user_id cannot be empty"}
        elif not user:
            return {"statusCode": response_codes["USER_NOT_FOUND"], "message": "User not found"}
        else:
            cursor.execute("INSERT INTO prayers (prayer, scripture, user_id, category) VALUES (%s, %s, %s, %s)", (prayer, scripture, user_id, category))
            connection.commit()
    
            cursor.close()
            connection.close()
            response = {
                "statusCode": response_codes["SUCCESS"],
                "message": "Prayer added successfully",
                'data': {
                    "prayer": prayer,
                    "scripture": scripture,
                    "user_id": user_id,
                    "category": category,
                },
            }
            return response
    
        
    def get_prayers(self,request): 
        """
            name: get_prayers
            params: request
            description: get all prayers
            dependencies:psycopg2
            references:
        """
        connection = self.get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM prayers")
        prayers = cursor.fetchall()
        cursor.close()
        connection.close()
        response = {
            "statusCode": response_codes["SUCCESS"],
            "message": "Prayers retrieved successfully",
            'data': [
                {
                    "prayer": prayer[1],
                    "scripture": prayer[2],
                    "user_id": prayer[3],
                    "category": prayer[4],
                    "date_added": prayer[5]
                } for prayer in prayers
            ]
        }
        return response
    
    def get_prayer_by_id(self,request):
        """
            name: get_prayer_by_id
            params: request
            description: get prayer by id
            dependencies:psycopg2
            references:
        """
        data = request.json
        prayer_id = data.get('prayer_id')
        connection = self.get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM prayers WHERE id = %s", (prayer_id,))
        prayer = cursor.fetchone()
        cursor.close()
        connection.close()
        if not prayer:
            return {"statusCode": response_codes["INTERNAL_ERROR"], "message": "Prayer not found"}
        response = {
            "statusCode": response_codes["SUCCESS"],
            "message": "Prayer retrieved successfully",
            'data': {
                "id": prayer[0],
                "prayer": prayer[1],
                "scripture": prayer[2],
                "user_id": prayer[3],
                "category": prayer[4],
                "date_added": prayer[5]
            }
        }
        return response