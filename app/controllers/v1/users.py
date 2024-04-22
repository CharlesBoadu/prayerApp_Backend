from app.main import app
from flask import jsonify, request
from app.config import (response_codes)
from app.services.v1.users_service import UsersService
import json
from app.config import (CODE_SUCCESS, CODE_FAILURE, CODE_SERVICE_INTERNAL_ERROR, en)
from app.libs.decorators import Decorators

required_params = Decorators()

@app.route('/api/v1/users', methods=['GET'])
def getUsers():
    getUsersService = UsersService()
    result = getUsersService.get_users(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401
    

@app.route('/api/v1/user', methods=['POST'])
@required_params.required_params('user_id', 'organization_id')    
def getUserById():
    try:
        if request.method == 'POST':
            app_user_service = UsersService()
            result = app_user_service.get_user(request)
            
            return jsonify(result), 200

    except KeyError as ex:
        # Logger.log_to_console(__name__, "ERROR", "KeyError: {}".format(ex), CODE_FAILURE, "")
        return jsonify(code=CODE_FAILURE, msg=en['MISSING_PARAMETER'].format(str(ex))), 500

    except Exception as ex:
        print("Ex", ex)
        # Logger.log_to_console(__name__, "ERROR", "Exception: {}".format(ex), CODE_FAILURE, "")
        return jsonify(code=CODE_SERVICE_INTERNAL_ERROR, message=en['ERROR_OCCURRED'].format(str(ex))), 500


@app.route('/api/v1/users/organization', methods=['POST'])
def getUsersByOrganization():
    getUsersService = UsersService()
    result = getUsersService.get_users_by_organization(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401
    
@app.route('/api/v1/user/<int:id>', methods=['DELETE'])
def deleteUser(id):
    deleteUserService = UsersService()
    result = deleteUserService.delete_user(request,id)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401
    
@app.route('/api/v1/user/<int:id>', methods=['PUT'])
def updateUser(id):
    updateUserService = UsersService()
    result = updateUserService.update_user(request,id)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401
    