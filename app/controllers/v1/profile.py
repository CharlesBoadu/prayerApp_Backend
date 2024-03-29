from app.main import app
from flask import jsonify, request
from app.config import (response_codes)
from app.services.v1.update_password_service import UpdatePasswordService
from app.services.v1.update_profile_service import UpdateProfileService


@app.route('/api/v1/profile/update/<int:id>', methods=['PUT'])
def updateProfile(id):
    updateProfileService = UpdateProfileService()
    result = updateProfileService.update_profile(request, id)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401
    
@app.route('/api/v1/profile/update_password/<int:id>', methods=['PUT'])
def updatePassword(id):
    updatePasswordService = UpdatePasswordService()
    result = updatePasswordService.update_password(request, id)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401