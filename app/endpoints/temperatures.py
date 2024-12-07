from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime
from models import temperaturi, orase, tari

tmp_bp = Blueprint('temperatures', __name__)

def contains_all_fields(data):
    # Check if the required fields are present in the data
    if not data or "idOras" not in data or "valoare" not in data:
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
    # Get the JSON body from the request
    data = request.json

    # Check if the required fields are present in the data
    if not contains_all_fields(data):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if the id is valid
    if not is_valid_id(data["idOras"]):
        return jsonify({"error": "Invalid city ID"}), 400

    # Check if the city exists
    if not find_entity_by_id(data["idOras"], "city"):
        return jsonify({"error": "City not found"}), 404
    
    # Check if temperature is a number
    if not isinstance(data["valoare"], (int, float)):
        return jsonify({"error": "Temperature is not a number"}), 400

    # Add the timestamp to the data
    data["timestamp"] = datetime.now()

    # Check if the temperature already exists for this timestamp
    if temperaturi.find_one({"idOras": data["idOras"], "timestamp": data["timestamp"]}):
        return jsonify({"error": "Temperature already exists for this timestamp"}), 409

    # Insert the new temperature into the database
    result = temperaturi.insert_one(data)

    # Return the ID of the newly inserted temperature
    return jsonify({"id": str(result.inserted_id)}), 201

def construct_date_query(from_date, until_date, temp_query):
    # Construct the timestamp query
    if from_date or until_date:
        temp_query["timestamp"] = {}
        if from_date:
            try:
                temp_query["timestamp"]["$gte"] = datetime.fromisoformat(from_date)
            except ValueError:
                return -1
        if until_date:
            try:
                temp_query["timestamp"]["$lte"] = datetime.fromisoformat(until_date)
            except ValueError:
                return -1

    return temp_query

def format_temperature_response(temperatures):
    # Format the response
    response = [
        {
            "id": str(temp["_id"]),
            "timestamp": temp["timestamp"].isoformat()
        }
        for temp in temperatures
    ]

    return jsonify(response), 200


def find_temperatures_for_cities(cities, from_date, until_date):
    temperatures = []
    for city in cities:
        temp_query = {"idOras": str(city["_id"])}

        if from_date or until_date:
            temp_query = construct_date_query(from_date, until_date, temp_query)

            if temp_query == -1:
                return jsonify({"error": "Invalid date format"}), 400
            
        temps = list(temperaturi.find(temp_query, {"_id": 1, "valoare": 1, "timestamp": 1}))
        temperatures.extend(temps)

    return temperatures

@tmp_bp.route('/api/temperatures', methods=['GET'])
def get_temperatures():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    from_date = request.args.get("from")
    until_date = request.args.get("until")

    # Check if no query parameters are provided
    if not lat and not lon and not from_date and not until_date:
        temperatures = list(temperaturi.find({}, {"_id": 1, "valoare": 1, "timestamp": 1}))
        for temp in temperatures:
            temp["id"] = str(temp.pop("_id"))
        return jsonify(temperatures), 200   
    
    # Cities starts as all cities
    cities = list(orase.find({}, {"_id": 1}))
    if lat or lon:
        # Find the city based on latitude and/or longitude
        city_query = {}
        if lat:
            city_query["lat"] = float(lat)
        if lon:
            city_query["lon"] = float(lon)

        # Find all the cities with the specified latitude and longitude
        cities = list(orase.find(city_query, {"_id": 1}))

    # Check if the city was found return empty list
    if not cities:
        return jsonify([]), 200
    
    # For each city in the list, find the temperatures
    temperatures = find_temperatures_for_cities(cities, from_date, until_date)

    # Check if no temperatures were found
    if not temperatures:
        return jsonify([]), 200

    # Format the response
    return format_temperature_response(temperatures)

@tmp_bp.route('/api/temperatures/cities/<idOras>', methods=['GET'])
def get_city_temperatures(idOras):
    # Check if the id is valid
    if not is_valid_id(idOras):
        return jsonify({"error": "Invalid city ID"}), 400

    # Check if the city exists return empty list
    city = find_entity_by_id(idOras, "city")
    if not city:
        return jsonify([]), 200

    # Parse the query parameters for date filtering
    from_date = request.args.get("from")
    until_date = request.args.get("until")

    # Construct the query
    temp_query = {"idOras": idOras}
    temp_query = construct_date_query(from_date, until_date, temp_query)

    if temp_query == -1:
        return jsonify({"error": "Invalid date format"}), 400

    # Find the temperatures for the city
    temperatures = list(temperaturi.find(temp_query, {"_id": 1, "valoare": 1, "timestamp": 1}))

    # Check if no temperatures were found
    if not temperatures:
        # Return empty list
        return jsonify([]), 200

    # Format the response
    return format_temperature_response(temperatures)

@tmp_bp.route('/api/temperatures/countries/<id_tara>', methods=['GET'])
def get_country_temperatures(id_tara):
    # print all countries in db
    with open("log.txt", "a") as f:
        f.write(f"{list(tari.find({}, {'_id': 1}))}\n")
    
    # Check if the id is valid
    if not is_valid_id(id_tara):
        return jsonify({"error": "Invalid country ID"}), 400

    # Check if the country exists return empty list
    country = find_entity_by_id(id_tara, "country")
    if not country:
        return jsonify([]), 200
    
    with open("log.txt", "a") as f:
        f.write(f"Found country: {country}\n")

    # Log all the cities and their country id
    with open("log.txt", "a") as f:
        f.write("All the cities in the database:\n")
        f.write(f"{list(orase.find({}, {'_id': 1, 'idTara': 1}))}\n")

    # Find all cities in the country
    cities = list(orase.find({"idTara": id_tara}, {"_id": 1}))

    with open("log.txt", "a") as f:
        f.write(f"Found cities: {cities}\n")

    # Parse the query parameters for date filtering
    from_date = request.args.get("from")
    until_date = request.args.get("until")

    # Foe each city in the list, find the temperatures
    temperatures = find_temperatures_for_cities(cities, from_date, until_date)

    with open("log.txt", "a") as f:
        f.write(f"Found temperatures: {temperatures}\n")

    # Check if no temperatures were found
    if not temperatures:
        return jsonify([]), 200

    # Format the response
    return format_temperature_response(temperatures)

@tmp_bp.route('/api/temperatures/<id>', methods=['PUT'])
def update_temperature(id):
    # Get the JSON data from the request
    data = request.json

    # Check if the required fields are present in the data
    if not contains_all_fields(data):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if the id is valid
    if not is_valid_id(id):
        return jsonify({"error": "Invalid temperature ID"}), 400

    # Check if the temperature exists
    if not temperaturi.find_one({"_id": ObjectId(id)}):
        return jsonify({"error": "Temperature not found"}), 404

    # Update the temperature with the specified ID
    result = temperaturi.update_one({"_id": ObjectId(id)}, {"$set": data})

    # Translate the idOras field to idOras
    data["idOras"] = data.pop("idOras")

    # Return a success message
    return jsonify({"message": "Temperature updated"}), 200

@tmp_bp.route('/api/temperatures/<id>', methods=['DELETE'])
def delete_temperature(id):
    # Check if id only contains alphanumeric characters
    if not id.isalnum():
        return jsonify({"error": "ID must contain only alphanumeric characters"}), 400

    # Check if the id is valid
    if not is_valid_id(id):
        return jsonify({"error": "Invalid temperature ID"}), 404

    # Delete the temperature with the specified ID
    result = temperaturi.delete_one({"_id": ObjectId(id)})

    # Check if the temperature was found and deleted
    if result.deleted_count == 0:
        return jsonify({"error": "Temperature not found"}), 404

    # Return a success message if the temperature was deleted
    return jsonify({"message": "Temperature deleted"}), 200


        