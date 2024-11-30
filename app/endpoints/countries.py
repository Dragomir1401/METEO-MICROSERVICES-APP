from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from models import tari

countries_bp = Blueprint('countries', __name__)

@countries_bp.route('/api/countries/clear', methods=['DELETE'])
def clear_countries():
    """Clear all countries from the database"""
    tari.delete_many({})
    return jsonify({"message": "All countries cleared"}), 200

@countries_bp.route('/api/countries', methods=['POST'])
def add_country():
    data = request.json
    if not data or "nume_tara" not in data or "latitudine" not in data or "longitudine" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    if tari.find_one({"nume_tara": data["nume_tara"]}):
        return jsonify({"error": "Country already exists"}), 409
    result = tari.insert_one(data)
    return jsonify({"id": str(result.inserted_id)}), 201


@countries_bp.route('/api/countries', methods=['GET'])
def get_countries():
    countries = list(tari.find({}, {"_id": 1, "nume_tara": 1, "latitudine": 1, "longitudine": 1}))
    for country in countries:
        country["id"] = str(country.pop("_id"))
    return jsonify(countries), 200


@countries_bp.route('/api/countries/<id>', methods=['PUT'])
def update_country(id):
    data = request.json
    if not data or "nume_tara" not in data or "latitudine" not in data or "longitudine" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    result = tari.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"error": "Country not found"}), 404
    return jsonify({"message": "Country updated"}), 200


@countries_bp.route('/api/countries/<id>', methods=['DELETE'])
def delete_country(id):
    result = tari.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Country not found"}), 404
    return jsonify({"message": "Country deleted"}), 200
