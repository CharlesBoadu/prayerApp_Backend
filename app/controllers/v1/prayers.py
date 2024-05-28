from app.main import app
from flask import jsonify, request
from app.config import (response_codes)
from app.services.v1.prayer_service import PrayerService
from app.libs.decorators import Decorators

jwt_token_required = Decorators()

@app.route('/api/v1/prayer/new', methods=['POST'])
@jwt_token_required.token_required
def addPrayer():
    addPrayerService = PrayerService()
    result = addPrayerService.add_prayer(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401
    

@app.route('/api/v1/prayers', methods=['GET'])
@jwt_token_required.token_required
def getPrayers():
    getPrayersService = PrayerService()
    result = getPrayersService.get_prayers(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401
    
@app.route('/api/v1/prayer', methods=['POST'])
@jwt_token_required.token_required
def getPrayerById():
    getPrayersService = PrayerService()
    result = getPrayersService.get_prayer_by_id(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401
    
@app.route('/api/v1/user/prayers', methods=['POST'])
@jwt_token_required.token_required
def getPrayersByUser():
    getPrayersService = PrayerService()
    result = getPrayersService.get_prayers_by_user_id(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401

@app.route('/api/v1/favorite-prayers', methods=['GET'])
@jwt_token_required.token_required
def getFavoritePrayers():
    getPrayersService = PrayerService()
    result = getPrayersService.get_favorite_prayers(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401

@app.route('/api/v1/favorite-prayers/new', methods=['POST'])
@jwt_token_required.token_required
def addPrayerToFavorites():
    getPrayersService = PrayerService()
    result = getPrayersService.add_prayer_to_favorites(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401
    
@app.route('/api/v1/user/favorite-prayers', methods=['POST'])
@jwt_token_required.token_required
def getFavoritePrayersByUser():
    getPrayersService = PrayerService()
    result = getPrayersService.get_favorite_prayers_by_user(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401
    
@app.route('/api/v1/user/favorite-prayers', methods=['DELETE'])
@jwt_token_required.token_required
def removeFavoritePrayer():
    getPrayersService = PrayerService()
    result = getPrayersService.remove_prayer_from_favorites(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401