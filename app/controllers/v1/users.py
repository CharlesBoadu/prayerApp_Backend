from app.main import app
from flask import jsonify, request
from app.config import (response_codes)
from app.services.v1.users_service import UsersService


@app.route('/api/v1/users', methods=['GET'])
def getUsers():
    getUsersService = UsersService()
    result = getUsersService.get_users(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401
    