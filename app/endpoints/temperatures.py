from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime
from models import temperaturi, orase, tari

tmp_bp = Blueprint('temperatures', __name__)

@tmp_bp.route('/api/temperatures/clear', methods=['DELETE'])
def clear_temperatures():
    """Clear all temperatures from the database"""
    temperaturi.delete_many({})
    return jsonify({"message": "All temperatures cleared"}), 200


@tmp_bp.route('/api/temperatures', methods=['POST'])
def add_temperature():
    data = request.json
    if not data or "id_oras" not in data or "valoare" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    if not orase.find_one({"_id": ObjectId(data["id_oras"])}):
        return jsonify({"error": "City not found"}), 404
    data["timestamp"] = datetime.utcnow()
    if temperaturi.find_one({"id_oras": data["id_oras"], "timestamp": data["timestamp"]}):
        return jsonify({"error": "Temperature already exists for this timestamp"}), 409
    result = temperaturi.insert_one(data)
    return jsonify({"id": str(result.inserted_id)}), 201


@tmp_bp.route('/api/temperatures', methods=['GET'])
def get_temperatures():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    from_date = request.args.get("from")
    until_date = request.args.get("until")

    query = {}
    if lat:
        query["latitudine"] = float(lat)
    if lon:
        query["longitudine"] = float(lon)
    if from_date or until_date:
        query["timestamp"] = {}
        if from_date:
            query["timestamp"]["$gte"] = datetime.fromisoformat(from_date)
        if until_date:
            query["timestamp"]["$lte"] = datetime.fromisoformat(until_date)

    temps = list(temperaturi.find(query, {"_id": 1, "valoare": 1, "timestamp": 1}))
    for temp in temps:
        temp["id"] = str(temp.pop("_id"))
    return jsonify(temps), 200


@tmp_bp.route('/api/temperatures/cities/<id_oras>', methods=['GET'])
def get_city_temperatures(id_oras):
    from_date = request.args.get("from")
    until_date = request.args.get("until")

    query = {"id_oras": id_oras}
    if from_date or until_date:
        query["timestamp"] = {}
        if from_date:
            query["timestamp"]["$gte"] = datetime.fromisoformat(from_date)
        if until_date:
            query["timestamp"]["$lte"] = datetime.fromisoformat(until_date)

    temps = list(temperaturi.find(query, {"_id": 1, "valoare": 1, "timestamp": 1}))
    for temp in temps:
        temp["id"] = str(temp.pop("_id"))
    return jsonify(temps), 200
