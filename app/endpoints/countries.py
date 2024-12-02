from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from models import orase, tari

cntrs_bp = Blueprint('countries', __name__)
template_fields = {"_id": 1, "nume_tara": 1, "latitudine": 1, "longitudine": 1}

def contains_all_fields(data):
    # Check if the required fields are present in the data
    if not data or "nume_tara" not in data or "latitudine" not in data or "longitudine" not in data:
        return False
    return True

def is_valid_id(id):
    # Check if the ID is a valid ObjectId
    if not ObjectId.is_valid(id):
        return False
    return True

@cntrs_bp.route('/api/countries/clear', methods=['DELETE'])
def clear_countries():
    # Use delete_many() method to delete all documents from the collection
    result = tari.delete_many({})
    
    # Return a response
    return jsonify({"message": "All countries cleared"}), 200

@cntrs_bp.route('/api/countries', methods=['POST'])
def add_country():
    # Get the JSON data from the request
    data = request.json

    # Check if the required fields are present in the data
    if not contains_all_fields(data):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if the country already exists and return an error if it does
    if tari.find_one({"nume_tara": data["nume_tara"]}):
        return jsonify({"error": "Country already exists"}), 409

    # Insert the new country into the database
    result = tari.insert_one(data)

    # Return the ID of the newly inserted country
    return jsonify({"id": str(result.inserted_id)}), 201


@cntrs_bp.route('/api/countries', methods=['GET'])
def get_countries():
    # Specify the fields to include in the response
    countries = list(tari.find({}, template_fields))

    # Translate all the fields to the required format
    for country in countries:
        country["id"] = str(country.pop("_id"))
        country["lat"] = country.pop("latitudine")
        country["lon"] = country.pop("longitudine")
        country["nume"] = country.pop("nume_tara")

    # Return the list of countries
    return jsonify(countries), 200


@cntrs_bp.route('/api/countries/<id>', methods=['PUT'])
def update_country(id):
    # Get the JSON data from the request
    data = request.json

    # Check if the required fields are present in the data
    if not contains_all_fields(data):
        return jsonify({"error": "Missing required fields"}), 400

    # Check for bad id
    if not is_valid_id(id):
        return jsonify({"error": "Invalid ID"}), 400

    # Update the country with the specified ID
    result = tari.update_one({"_id": ObjectId(id)}, {"$set": data})

    # Check if the country was found and updated
    if result.matched_count == 0:
        return jsonify({"error": "Country not found"}), 404

    # Return a success message
    return jsonify({"message": "Country updated"}), 200


@cntrs_bp.route('/api/countries/<id>', methods=['DELETE'])
def delete_country(id):
    # Check for 400 error
    if not is_valid_id(id):
        return jsonify({"error": "Invalid ID"}), 400
    
    # Find all cities in the country
    cities = orase.find({"id_tara": ObjectId(id)})
    city_ids = [str(city["_id"]) for city in cities]

    # Delete all temperatures for the cities in this country
    if city_ids:
        delete_temperatures_result = temperaturi.delete_many({"id_oras": {"$in": city_ids}})

        # Delete all cities in the country
        delete_cities_result = orase.delete_many({"id_tara": ObjectId(id)})
    
    # Delete the country itself
    result = tari.delete_one({"_id": ObjectId(id)})

    # Check if the country was found and deleted
    if result.deleted_count == 0:
        return jsonify({"error": "Country not found"}), 404

    # Return a success message if the country and related cities/temperatures were deleted
    return jsonify({"message": "Country, cities, and temperatures deleted"}), 200

