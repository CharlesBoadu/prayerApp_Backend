
from flask import Blueprint
from flask import jsonify, request
from app.config import (response_codes)
from app.services.v1.login_service import LoginService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/app/v1/login', methods=['POST'])
def login():
    loginService = LoginService()
    result = loginService.authenticate_user(request)
    if result.get("code") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401




