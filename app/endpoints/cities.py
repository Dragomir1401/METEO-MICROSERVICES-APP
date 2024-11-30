from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from models import orase, tari

cities_bp = Blueprint('cities', __name__)

@cities_bp.route('/api/cities/clear', methods=['DELETE'])
def clear_cities():
    """Clear all cities from the database"""
    orase.delete_many({})
    return jsonify({"message": "All cities cleared"}), 200

@cities_bp.route('/api/cities', methods=['POST'])
def add_city():
    data = request.json
    if not data or "id_tara" not in data or "nume_oras" not in data or "latitudine" not in data or "longitudine" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    if not tari.find_one({"_id": ObjectId(data["id_tara"])}):
        return jsonify({"error": "Country not found"}), 404
    if orase.find_one({"id_tara": data["id_tara"], "nume_oras": data["nume_oras"]}):
        return jsonify({"error": "City already exists in the country"}), 409
    result = orase.insert_one(data)
    return jsonify({"id": str(result.inserted_id)}), 201


@cities_bp.route('/api/cities', methods=['GET'])
def get_cities():
    cities = list(orase.find({}, {"_id": 1, "id_tara": 1, "nume_oras": 1, "latitudine": 1, "longitudine": 1}))
    for city in cities:
        city["id"] = str(city.pop("_id"))
    return jsonify(cities), 200


@cities_bp.route('/api/cities/<id>', methods=['PUT'])
def update_city(id):
    data = request.json
    if not data or "id_tara" not in data or "nume_oras" not in data or "latitudine" not in data or "longitudine" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    result = orase.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"error": "City not found"}), 404
    return jsonify({"message": "City updated"}), 200


@cities_bp.route('/api/cities/<id>', methods=['DELETE'])
def delete_city(id):
    result = orase.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"error": "City not found"}), 404
    return jsonify({"message": "City deleted"}), 200
