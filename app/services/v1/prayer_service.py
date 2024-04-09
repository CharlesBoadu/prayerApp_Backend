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
                    "id": prayer[0],
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
                "is_favorite": prayer[5],
                "date_added": prayer[6]
            }
        }
        return response
    
    def get_prayers_by_user_id(self,request):
        """
            name: get_prayers_by_user_id
            params: request
            description: get prayer by user_id
            dependencies:psycopg2
            references:
        """
        data = request.json
        user_id = data.get('user_id')
        connection = self.get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM prayers WHERE user_id = %s", (user_id,))
        prayers = cursor.fetchall()
        cursor.close()
        connection.close()
        if not prayers:
            return {"statusCode": response_codes["INTERNAL_ERROR"], "message": "Prayer not found"}
        response = {
            "statusCode": response_codes["SUCCESS"],
            "message": "Prayer retrieved successfully",
            'data': [
                {
                    "id": prayer[0],
                    "prayer": prayer[1],
                    "scripture": prayer[2],
                    "user_id": prayer[3],
                    "category": prayer[4],
                    "date_added": prayer[5]
                } for prayer in prayers
            ]
        }
        return response
    
    def add_prayer_to_favorites(self,request):
        """
            name: add_prayer_to_favorites
            params: request
            description: add_prayer_to_favorites
            dependencies:psycopg2
            references:
        """
        data = request.json
        user_id = data.get('user_id')
        prayer_id = data.get('prayer_id')
        prayer = data.get('prayer')
        scripture = data.get('scripture')
        category = data.get('category')

        connection = self.get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM prayers WHERE id = %s", (prayer_id,))
        existing_prayer = cursor.fetchone()

        if not existing_prayer:
            return {"statusCode": response_codes["INTERNAL_ERROR"], "message": "Prayer Not Found"}
        else:
            cursor.execute("SELECT * FROM favorite_prayers WHERE id = %s", (prayer_id,))
            favorite_prayer = cursor.fetchone()

            if favorite_prayer:
                return {"statusCode": response_codes["ALREADY_EXIST"], "message": "Prayer already added to Favorites"}
            
            cursor.execute("INSERT INTO favorite_prayers (id, prayer, scripture, user_id, category) VALUES (%s, %s, %s, %s, %s)", (prayer_id, prayer, scripture, user_id, category))
            connection.commit()

            cursor.close()
            connection.close()

            response = {
                "statusCode": response_codes["SUCCESS"],
                "message": "Prayer added to Favorites successfully",
                'data': {
                        "prayer": prayer,
                        "scripture": scripture,
                        "user_id": user_id,
                        "category": category,
                    },
            }
            return response
        
    def get_favorite_prayers(self,request): 
        """
            name: get_favorite_prayers
            params: request
            description: get all Favorite prayers
            dependencies:psycopg2
            references:
        """
        connection = self.get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM favorite_prayers")
        prayers = cursor.fetchall()
        
        cursor.close()
        connection.close()
        if not prayers:
            return {"statusCode": response_codes["SUCCESS"], "message": "Favorite Prayers retrieved successfully", "data": []}
        response = {
            "statusCode": response_codes["SUCCESS"],
            "message": "Favorite Prayers retrieved successfully",
            'data': [
                {
                    "id": prayer[0],
                    "prayer": prayer[1],
                    "scripture": prayer[2],
                    "user_id": prayer[3],
                    "category": prayer[4],
                    "date_added": prayer[5]
                } for prayer in prayers
            ]
        }
        return response
    
    def get_favorite_prayers_by_user(self,request): 
        """
            name: get_favorite_prayers_by_user
            params: request
            description: get all Favorite prayers by User
            dependencies:psycopg2
            references:
        """
        connection = self.get_db_connection()
        cursor = connection.cursor()
        data = request.json
        user_id = data.get('user_id')

        cursor.execute("SELECT * FROM favorite_prayers WHERE user_id = %s", (user_id,))
        prayers = cursor.fetchall()
        
        cursor.close()
        connection.close()
        if not prayers:
            return {"statusCode": response_codes["SUCCESS"], "message": "Favorite Prayers By User retrieved successfully", "data": []}
        response = {
            "statusCode": response_codes["SUCCESS"],
            "message": "Favorite Prayers by user retrieved successfully",
            'data': [
                {
                    "id": prayer[0],
                    "prayer": prayer[1],
                    "scripture": prayer[2],
                    "user_id": prayer[3],
                    "category": prayer[4],
                    "date_added": prayer[5]
                } for prayer in prayers
            ]
        }
        return response