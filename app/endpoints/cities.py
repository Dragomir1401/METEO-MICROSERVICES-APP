from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from models import orase, tari, temperaturi

ct_bp = Blueprint('cities', __name__)

def contains_all_fields(data):
    # Check if the required fields are present in the data
    if not data or "idTara" not in data or "nume" not in data or "lat" not in data or "lon" not in data:
        return False
    return True

def is_valid_id(id):
    # Check if the ID is a valid ObjectId
    if not ObjectId.is_valid(id):
        return False
    return True

def find_entity_by_id(id, countryOrCity):
    # Find the city with the specified ID based on the countryOrCity parameter
    if countryOrCity == "country":
        return tari.find_one({"_id": ObjectId(id)})
    elif countryOrCity == "city":
        return orase.find_one({"_id": ObjectId(id)})
    return None

def translate_fields(city):
    # Translate all the fields to the required format
    city["id"] = str(city.pop("_id"))

@ct_bp.route('/api/cities/clear', methods=['DELETE'])
def clear_cities():
    # Clear all cities from the database
    orase.delete_many({})
    return jsonify({"message": "All cities cleared"}), 200

@ct_bp.route('/api/cities', methods=['POST'])
def add_city():
    # Get the JSON data from the request
    data = request.json

    # Check if the required fields are present in the data
    if not contains_all_fields(data):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if the id of the country is a valid ObjectId
    if not is_valid_id(data["idTara"]):
        return jsonify({"error": "Invalid country ID"}), 400

    # Check if the country exists
    if find_entity_by_id(data["idTara"], "country") is None:
        return jsonify({"error": "Country not found"}), 404

    # Check if the city already exists in the country
    if orase.find_one({"idTara": data["idTara"], "nume": data["nume"]}):
        return jsonify({"error": "City already exists in the country"}), 409

    # Insert the new city into the database
    result = orase.insert_one(data)

    # Return the ID of the newly inserted city
    return jsonify({"id": str(result.inserted_id)}), 201


@ct_bp.route('/api/cities', methods=['GET'])
def get_cities():
    # Specify the fields to include in the response
    cities = list(orase.find({}, {"_id": 1, "idTara": 1, "nume": 1, "lat": 1, "lon": 1}))

    # Translate all the fields to the required format
    for city in cities:
        translate_fields(city)

    # Return the list of cities
    return jsonify(cities), 200

@ct_bp.route('/api/cities/country/<idTara>', methods=['GET'])
def get_cities_by_country(idTara):
    # Check if the id of the country is a valid ObjectId
    if not is_valid_id(idTara):
        return jsonify({"error": "Invalid country ID"}), 400

    # Check if city exists
    if find_entity_by_id(idTara, "country") is None:
        return jsonify({"error": "Country not found"}), 404

    # Get the cities for the specified country
    cities = list(orase.find({"idTara": idTara}, {"_id": 1, "nume": 1, "lat": 1, "lon": 1}))

    # Translate all the fields to the required format
    for city in cities:
        translate_fields(city)

    # Return the list of cities
    return jsonify(cities), 200


@ct_bp.route('/api/cities/<id>', methods=['PUT'])
def update_city(id):
    # Get the JSON data from the request
    data = request.json

    # Check if the required fields are present in the data
    if not contains_all_fields(data):
        return jsonify({"error": "Missing required fields"}), 400

    # Check for invalid country ID
    if not is_valid_id(data["idTara"]):
        return jsonify({"error": "Invalid country ID"}), 400
    
    # Check if the country exists
    if find_entity_by_id(data["idTara"], "country") is None:
        return jsonify({"error": "Country not found"}), 404

    # Check for bad id
    if not is_valid_id(id):
        return jsonify({"error": "Invalid city ID to be updated"}), 400
    
    # Check for bad id
    if "id" in data and not is_valid_id(data["id"]):
        return jsonify({"error": "Invalid city ID to update with"}), 400
    
    # Check if the city already exists by name in that country
    if orase.find_one({"idTara": data["idTara"], "nume": data["nume"]}):
        return jsonify({"error": "City already exists in the country"}), 409

    # Update the city with the specified ID
    result = orase.update_one({"_id": ObjectId(id)}, {"$set": data})

    # Check if the city exists and was updated
    if result.matched_count == 0:
        return jsonify({"error": "City not found"}), 404

    # Return a success message
    return jsonify({"message": "City updated"}), 200


@ct_bp.route('/api/cities/<id>', methods=['DELETE'])
def delete_city(id):
    # Check if id only contains alphanumeric characters
    if not id.isalnum():
        return jsonify({"error": "ID must contain only alphanumeric characters"}), 400
    
    # Check if id is a valid ObjectId
    if not is_valid_id(id):
        return jsonify({"error": "Invalid city ID"}), 404

    # Delete all temperatures for the city
    temperaturi.delete_many({"idOras": {"$in": [ObjectId(id)]}})

    # Delete the city with the specified ID
    result = orase.delete_one({"_id": ObjectId(id)})

    # Check if the city was found and deleted
    if result.deleted_count == 0:
        return jsonify({"error": "City not found"}), 404

    # Return a success message if the city was deleted
    return jsonify({"message": "City deleted"}), 200
