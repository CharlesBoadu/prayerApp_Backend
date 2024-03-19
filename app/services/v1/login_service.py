import os
import psycopg2
from flask import Flask, request, jsonify
import bcrypt
from werkzeug.security import check_password_hash
from app.config import response_codes

class LoginService:
    def get_db_connection():
        """
        name: get_db_connection
        params: null
        description: connect to postgresql db using psycopg2
        dependencies:psycopg2
        references:
        """
        conn = psycopg2.connect(host='localhost',
                                database='prayer_app',
                                user=os.environ['DB_USERNAME'],
                                password=os.environ['DB_PASSWORD'])
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
        username = data.get('username')
        password = data.get('password')
        connection = self.get_db_connection()
        cursor = connection.cursor()

        user = cursor.execute("SELECT * FROM users WHERE username = %s", (username,))

         # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            return {"code": response_codes["INTERNAL_ERROR"], "message": "User not found"}
        # return redirect(url_for('auth.login'))



        
        # Fetch the hashed password from the database based on the username
        # cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        # stored_password_hash = cursor.fetchone()
        # connection.close()

        # if stored_password_hash:
        #     stored_password_hash = stored_password_hash[0]

        #     #Verify the entered password against the stored hashed pasword
        #     if bcrypt.checkpw(password.encode('utf-8'),stored_password_hash.encode('utf-8')): 
        #         #Passwords match,fetch user information
        #         connection = self.get_db_connection()
        #         cursor = connection.cursor()

        #         #Join users,roles and user_permissions tables to get user information
        #         sql = "SELECT users.id, users.username,users.first_name,users.last_name,users.email,users.phone,users.country,users.region,users.city,users.branch,user_roles.role_name, permissions.permission FROM users INNER JOIN user_roles ON users.username = user_roles.user_name INNER JOIN permissions ON permissions.permission = user_roles.permission_name WHERE users.username = %s GROUP BY users.id, users.username,users.first_name,users.last_name,users.email,users.phone,users.country,users.region,users.city,users.branch,user_roles.role_name, permissions.permission"


        #         cursor.execute(sql, (username,))
        #         user = cursor.fetchone()

        #         cursor.close()
        #         connection.close()

        #         if user:
        #             user_id ,username,first_name,last_name,email,phone,country,region,city,branch,role,permissions = user
        #             permissions_list = [permissions] if permissions else []

        #             response_data = {
        #                 "code": response_codes["SUCCESS"],
        #                 "message": "Login successful",
        #                 'info': {
        #                     "user_id": user_id,
        #                     "username": username,
        #                     "first name":first_name,
        #                     "last name": last_name,
        #                     "email":email,
        #                     "phone":phone,
        #                     "country":country,
        #                     "region":region,
        #                     "city":city,
        #                     "branch":branch,
        #                     "role": role,
        #                     "permissions": permissions_list
        #                 },
        #             }
        #             return response_data
        #         else:
        #             return {"code": response_codes["INTERNAL_ERROR"], "message": "User not found"}
        #     else:
        #         return {"code": response_codes["INTERNAL_ERROR"], "message": "Invalid credentials"}
        # else:
        #     return {"code": response_codes["REQUEST_ERROR"], "message": "Request Error"}