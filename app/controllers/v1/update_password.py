from app.main import app
from flask import jsonify, request
from app.config import (response_codes)
from app.services.v1.update_password_service import UpdatePasswordService


@app.route('/app/v1/profile/update_password/<int:id>', methods=['PUT'])
def updatePassword(id):
    updatePasswordService = UpdatePasswordService()
    result = updatePasswordService.update_password(request, id)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401