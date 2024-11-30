from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from models import orase, tari

ct_bp = Blueprint('cities', __name__)

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
    if not data or "id_tara" not in data or "nume_oras" not in data or "latitudine" not in data or "longitudine" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    # Check if the id of the country is a valid ObjectId
    if not ObjectId.is_valid(data["id_tara"]):
        return jsonify({"error": "Invalid country ID"}), 400

    # Check if the country exists
    if not tari.find_one({"_id": ObjectId(data["id_tara"])}):
        return jsonify({"error": "Country not found"}), 404

    # Check if the city already exists in the country
    if orase.find_one({"id_tara": data["id_tara"], "nume_oras": data["nume_oras"]}):
        return jsonify({"error": "City already exists in the country"}), 409

    # Insert the new city into the database
    result = orase.insert_one(data)

    # Return the ID of the newly inserted city
    return jsonify({"id": str(result.inserted_id)}), 201


@ct_bp.route('/api/cities', methods=['GET'])
def get_cities():
    # Specify the fields to include in the response
    cities = list(orase.find({}, {"_id": 1, "id_tara": 1, "nume_oras": 1, "latitudine": 1, "longitudine": 1}))

    # Translate all the fields to the required format
    for city in cities:
        city["id"] = str(city.pop("_id"))
        city["idTara"] = city.pop("id_tara")
        city["nume"] = city.pop("nume_oras")
        city["lat"] = city.pop("latitudine")
        city["lon"] = city.pop("longitudine")

    # Return the list of cities
    return jsonify(cities), 200

@ct_bp.route('/api/cities/country/<id_tara>', methods=['GET'])
def get_cities_by_country(id_tara):
    # Check if the id of the country is a valid ObjectId
    if not ObjectId.is_valid(id_tara):
        return jsonify({"error": "Invalid country ID"}), 400

    # Check if city exists
    if not tari.find_one({"_id": ObjectId(id_tara)}):
        return jsonify({"error": "Country not found"}), 404

    # Get the cities for the specified country
    cities = list(orase.find({"id_tara": id_tara}, {"_id": 1, "nume_oras": 1, "latitudine": 1, "longitudine": 1}))

    # Translate all the fields to the required format
    for city in cities:
        city["idTara"] = id_tara
        city["id"] = str(city.pop("_id"))
        city["nume"] = city.pop("nume_oras")
        city["lat"] = city.pop("latitudine")
        city["lon"] = city.pop("longitudine")

    # Return the list of cities
    return jsonify(cities), 200


@ct_bp.route('/api/cities/<id>', methods=['PUT'])
def update_city(id):
    # Get the JSON data from the request
    data = request.json

    # Check if the required fields are present in the data
    if not data or "id_tara" not in data or "nume_oras" not in data or "latitudine" not in data or "longitudine" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    # Check if the country exists
    if not tari.find_one({"_id": ObjectId(data["id_tara"])}):
        return jsonify({"error": "Country not found"}), 404

    # Check for bad id
    if not ObjectId.is_valid(id):
        return jsonify({"error": "Invalid city ID"}), 400

    # Update the city with the specified ID
    result = orase.update_one({"_id": ObjectId(id)}, {"$set": data})

    # Check if the city exists and was updated
    if result.matched_count == 0:
        return jsonify({"error": "City not found"}), 404

    # Return a success message
    return jsonify({"message": "City updated"}), 200


@ct_bp.route('/api/cities/<id>', methods=['DELETE'])
def delete_city(id):
    # Check if id is a valid ObjectId
    if not ObjectId.is_valid(id):
        return jsonify({"error": "Invalid city ID"}), 400

    # Delete the city with the specified ID
    result = orase.delete_one({"_id": ObjectId(id)})

    # Check if the city was found and deleted
    if result.deleted_count == 0:
        return jsonify({"error": "City not found"}), 404

    # Return a success message if the city was deleted
    return jsonify({"message": "City deleted"}), 200
