from app.main import app
from flask import jsonify, request
from app.config import (response_codes)
from app.services.v1.auth_service import LoginService
from app.services.v1.auth_service import RegisterService
from app.services.v1.auth_service import ResetPasswordService
from app.services.v1.auth_service import UpdatePasswordService

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
    
