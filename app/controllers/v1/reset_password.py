from app.main import app
from flask import jsonify, request
from app.config import (response_codes)
from app.services.v1.reset_password_service import ResetPasswordService


@app.route('/app/v1/reset_password_email', methods=['POST'])
def login():
    resetPasswordService = ResetPasswordService()
    result = resetPasswordService.send_reset_password(request)
    if result.get("code") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401