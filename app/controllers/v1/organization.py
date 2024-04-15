from app.main import app
from flask import jsonify, request
from app.config import (response_codes)
from app.services.v1.organization_service import OrganizationService

@app.route('/api/v1/organizations', methods=['GET'])
def getOrganzations():
    getOrganzationsService = OrganizationService()
    result = getOrganzationsService.get_organizations(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401
    
@app.route('/api/v1/organization', methods=['POST'])
def getOrganizationById():
    getOrganzationsService = OrganizationService()
    result = getOrganzationsService.get_organzation_by_id(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401