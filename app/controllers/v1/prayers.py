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

@app.route('/api/v1/favorite_prayers', methods=['GET'])
def getFavoritePrayers():
    getPrayersService = PrayerService()
    result = getPrayersService.get_favorite_prayers(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401

@app.route('/api/v1/favorite_prayers/new', methods=['POST'])
def addPrayerToFavorites():
    getPrayersService = PrayerService()
    result = getPrayersService.add_prayer_to_favorites(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401
    
@app.route('/api/v1/user/favorite_prayers', methods=['POST'])
def getFavoritePrayersByUser():
    getPrayersService = PrayerService()
    result = getPrayersService.get_favorite_prayers_by_user(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401
    
@app.route('/api/v1/user/favorite_prayers', methods=['DELETE'])
def removeFavoritePrayer():
    getPrayersService = PrayerService()
    result = getPrayersService.remove_prayer_from_favorites(request)
    if result.get("statusCode") == response_codes["SUCCESS"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401