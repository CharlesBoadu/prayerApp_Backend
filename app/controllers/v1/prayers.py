from app.main import app
from flask import jsonify, request
from app.config import (response_codes)
from app.services.v1.prayer_service import PrayerService


@app.route('/api/v1/prayer/new', methods=['POST'])
def addPrayer():
    addPrayerService = PrayerService()
    result = addPrayerService.add_prayer(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401
    

@app.route('/api/v1/prayers', methods=['GET'])
def getPrayers():
    getPrayersService = PrayerService()
    result = getPrayersService.get_prayers(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401
    
@app.route('/api/v1/prayer', methods=['POST'])
def getPrayerById():
    getPrayersService = PrayerService()
    result = getPrayersService.get_prayer_by_id(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401
    
@app.route('/api/v1/user/prayers', methods=['POST'])
def getPrayersByUser():
    getPrayersService = PrayerService()
    result = getPrayersService.get_prayers_by_user_id(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401