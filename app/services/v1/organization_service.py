import os
from dotenv import load_dotenv
import psycopg2
from app.config import response_codes


# Load environment variables from .env file
load_dotenv()

class OrganizationService:
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
    
    def get_organizations(self,request): 
        """
            name: get_organizations
            params: request
            description: get all organizations
            dependencies:psycopg2
            references:
        """
        connection = self.get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT organization, organization_id FROM users")
        organizations = cursor.fetchall()

        # Dictionary to store unique organizations
        unique_organizations = {}

        for name, identifier in organizations:
            normalized_name = name.lower()  # Normalize name to lowercase for case-insensitive comparison
            if normalized_name not in unique_organizations:
                unique_organizations[normalized_name] = {
                    "organization": name,
                    "organization_id": identifier
                }

        # Convert unique organizations dictionary values to a list
        unique_organizations_list = list(unique_organizations.values())

        print(organizations)
        response = {
                        "statusCode": response_codes["SUCCESS"],
                        "message": "Organizations retrieved successfully",
                        'data': unique_organizations_list,
                    }

        return response
    
    def get_organzation_by_id(self,request): 
        """
            name: get_organzation_by_id
            params: request
            description: get Organization by id
            dependencies:psycopg2
            references:
        """
        connection = self.get_db_connection()
        cursor = connection.cursor()

        data = request.json
        organzation_id = data.get("organization_id")

        cursor.execute("SELECT organization, organization_id FROM users WHERE organization_id = %s", (organzation_id,))
        organzation = cursor.fetchone()
        if organzation_id:
            response = {
                "statusCode": response_codes["SUCCESS"],
                "message": "Organzation retrieved successfully",
                'data': {
                    "Organization": organzation[0],
                    "Organization_id": organzation[1],
                }
            }
            return response
        else:
            return {"statusCode": response_codes["NOT_FOUND"], "message": "Organization does not exist"}
    