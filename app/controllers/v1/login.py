from app.main import app
from flask import jsonify, request
from app.config import (response_codes)
from app.services.v1.login_service import LoginService


@app.route('/app/v1/login', methods=['POST'])
def login():
    loginService = LoginService()
    result = loginService.authenticate_user(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401