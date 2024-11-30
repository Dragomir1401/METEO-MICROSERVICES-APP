from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime
from models import temperaturi, orase, tari

tmp_bp = Blueprint('temperatures', __name__)

def contains_all_fields(data):
    # Check if the required fields are present in the data
    if not data or "id_oras" not in data or "valoare" not in data:
        return False
    return True

def is_valid_id(id):
    # Check if the ID is a valid ObjectId
    if not ObjectId.is_valid(id):
        return False
    return True

@tmp_bp.route('/api/temperatures/clear', methods=['DELETE'])
def clear_temperatures():
    # Clear all temperatures from the database
    temperaturi.delete_many({})
    return jsonify({"message": "All temperatures cleared"}), 200

def find_entity_by_id(id, countryOrCity):
    # Find the city with the specified ID based on the countryOrCity parameter
    if countryOrCity == "country":
        return tari.find_one({"_id": ObjectId(id)})
    elif countryOrCity == "city":
        return orase.find_one({"_id": ObjectId(id)})
    return None


@tmp_bp.route('/api/temperatures', methods=['POST'])
def add_temperature():
    # Get the JSON data from the request
    data = request.json

    # Check if the required fields are present in the data
    if not contains_all_fields(data):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if the id is valid
    if not is_valid_id(data["id_oras"]):
        return jsonify({"error": "Invalid city ID"}), 400

    # Check if the city exists
    if not find_entity_by_id(data["id_oras"], "city"):
        return jsonify({"error": "City not found"}), 404

    # Add the timestamp to the data
    data["timestamp"] = datetime.utcnow()

    # Check if the temperature already exists for this timestamp
    if temperaturi.find_one({"id_oras": data["id_oras"], "timestamp": data["timestamp"]}):
        return jsonify({"error": "Temperature already exists for this timestamp"}), 409

    # Insert the new temperature into the database
    result = temperaturi.insert_one(data)

    # Return the ID of the newly inserted temperature
    return jsonify({"id": str(result.inserted_id)}), 201

@tmp_bp.route('/api/temperatures', methods=['GET'])
def get_temperatures():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    from_date = request.args.get("from")
    until_date = request.args.get("until")

    # Check if no query parameters are provided
    if not lat and not lon:
        temperatures = list(temperaturi.find({}, {"_id": 1, "valoare": 1, "timestamp": 1}))
        for temp in temperatures:
            temp["id"] = str(temp.pop("_id"))
        return jsonify(temperatures), 200

    # Find the city based on latitude and/or longitude
    city_query = {}
    if lat:
        city_query["latitudine"] = float(lat)
    if lon:
        city_query["longitudine"] = float(lon)

    # Run the query
    city = orase.find_one(city_query)

    # Check if the city was found
    if not city:
        return jsonify({"error": "City not found"}), 404

    # Extract the city ID from ObjectId
    city_id = str(city["_id"])

    # Find temperatures for the city
    temp_query = {"id_oras": city_id}
    if from_date or until_date:
        temp_query["timestamp"] = {}
        if from_date:
            temp_query["timestamp"]["$gte"] = datetime.fromisoformat(from_date)
        if until_date:
            temp_query["timestamp"]["$lte"] = datetime.fromisoformat(until_date)

    temperatures = list(temperaturi.find(temp_query, {"_id": 1, "valoare": 1, "timestamp": 1}))

    # Check if no temperatures were found
    if not temperatures:
        return jsonify({"error": "No matching temperatures found"}), 404

    # Format the response
    response = [
        {
            "id": str(temp["_id"]),
            "valoare": temp["valoare"],
            "timestamp": temp["timestamp"]
        }
        for temp in temperatures
    ]

    return jsonify(response), 200
  

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
