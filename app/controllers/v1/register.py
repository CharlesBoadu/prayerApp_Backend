from app.main import app
from flask import jsonify, request
from app.config import (response_codes)
from app.services.v1.register_service import RegisterService


@app.route('/app/v1/register', methods=['POST'])
def register():
    registerService = RegisterService()
    result = registerService.register_user(request)
    if result.get("code") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401