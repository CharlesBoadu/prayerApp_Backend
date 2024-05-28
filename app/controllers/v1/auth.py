from app.main import app
import json
from flask import jsonify, request
from app.config import (response_codes, CODE_SERVICE_INTERNAL_ERROR, CODE_FAILURE, en)
from app.services.v1.auth_service import LoginService
from app.services.v1.auth_service import RegisterService
from app.services.v1.auth_service import ResetPasswordService
from app.services.v1.auth_service import PassportService
from app.services.v1.auth_service import UpdatePasswordService
from app.libs.decorators import Decorators

jwt_token_required = Decorators()
required_params = Decorators()

@app.route('/api/v1/fetch-token', methods=['POST'])
@required_params.required_params('username', 'password','client_id')
def getToken():
    try:
        if request.method == 'POST':
            passport_services = PassportService()
            param  = json.loads(request.data.decode('utf-8'))
            result = passport_services.fetch_auth_token(param)
          
            return jsonify(**result), 200

    except Exception as ex:
       
        # Logger.log_to_console(__name__, "ERROR", "Exception: {}".format(ex), CODE_FAILURE, "")
        return jsonify(code=CODE_SERVICE_INTERNAL_ERROR, msg=en['ERROR_OCCURRED'].format(str(ex))), 500
    
@app.route('/api/v1/register', methods=['POST'])
def register():
    registerService = RegisterService()
    result = registerService.register_user(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401
    
@app.route('/api/v1/user/register', methods=['POST'])
def registeration_by_admin():
    registerService = RegisterService()
    result = registerService.register_user_by_admin(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401

@app.route('/api/v1/login', methods=['POST'])
@jwt_token_required.token_required
def login():
    loginService = LoginService()
    result = loginService.authenticate_user(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401
    
@app.route('/api/v1/reset-password-email', methods=['POST'])
def send_reset_password():
    resetPasswordService = ResetPasswordService()
    result = resetPasswordService.send_reset_password(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401
    
@app.route('/api/v1/reset-password', methods=['PUT'])
def reset_password():
    resetPasswordService = ResetPasswordService()
    result = resetPasswordService.reset_password(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401
    
