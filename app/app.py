from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://db:27017/")  # Use "db" as the MongoDB hostname (from Docker Compose)
db = client["weather_db"]

# Error response utility
def error_response(message, status_code):
    return jsonify({"error": message}), status_code

# --- Clear Database ---
@app.route('/api/countries/clear', methods=['DELETE'])
def clear_countries():
    db.countries.delete_many({})
    return jsonify({"message": "All countries cleared"}), 200

@app.route('/api/cities/clear', methods=['DELETE'])
def clear_cities():
    db.cities.delete_many({})
    return jsonify({"message": "All cities cleared"}), 200

# --- Countries Endpoints ---
@app.route('/api/countries', methods=['POST'])
def add_country():
    data = request.json
    if not data or "nume" not in data or "lat" not in data or "lon" not in data:
        return error_response("Missing required fields", 400)
    if db.countries.find_one({"nume": data["nume"]}):
        return error_response("Country already exists", 409)
    result = db.countries.insert_one(data)
    return jsonify({"id": str(result.inserted_id)}), 201


@app.route('/api/countries', methods=['GET'])
def get_countries():
    countries = list(db.countries.find({}, {"_id": 1, "nume": 1, "lat": 1, "lon": 1}))
    for country in countries:
        country["id"] = str(country.pop("_id"))
    return jsonify(countries), 200


@app.route('/api/countries/<id>', methods=['PUT'])
def update_country(id):
    data = request.json
    if not data or "nume" not in data or "lat" not in data or "lon" not in data:
        return error_response("Missing required fields", 400)
    result = db.countries.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.matched_count == 0:
        return error_response("Country not found", 404)
    return jsonify({"message": "Country updated"}), 200


@app.route('/api/countries/<id>', methods=['DELETE'])
def delete_country(id):
    result = db.countries.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return error_response("Country not found", 404)
    return jsonify({"message": "Country deleted"}), 200


# --- Cities Endpoints ---
@app.route('/api/cities', methods=['POST'])
def add_city():
    data = request.json
    if not data or "idTara" not in data or "nume" not in data or "lat" not in data or "lon" not in data:
        return error_response("Missing required fields", 400)
    if not db.countries.find_one({"_id": ObjectId(data["idTara"])}):
        return error_response("Country not found", 404)
    if db.cities.find_one({"nume": data["nume"], "idTara": data["idTara"]}):
        return error_response("City already exists in the country", 409)
    result = db.cities.insert_one(data)
    return jsonify({"id": str(result.inserted_id)}), 201


@app.route('/api/cities', methods=['GET'])
def get_cities():
    cities = list(db.cities.find({}, {"_id": 1, "idTara": 1, "nume": 1, "lat": 1, "lon": 1}))
    for city in cities:
        city["id"] = str(city.pop("_id"))
    return jsonify(cities), 200


@app.route('/api/cities/country/<idTara>', methods=['GET'])
def get_cities_by_country(idTara):
    cities = list(db.cities.find({"idTara": idTara}, {"_id": 1, "idTara": 1, "nume": 1, "lat": 1, "lon": 1}))
    for city in cities:
        city["id"] = str(city.pop("_id"))
    return jsonify(cities), 200


@app.route('/api/cities/<id>', methods=['PUT'])
def update_city(id):
    data = request.json
    if not data or "idTara" not in data or "nume" not in data or "lat" not in data or "lon" not in data:
        return error_response("Missing required fields", 400)
    result = db.cities.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.matched_count == 0:
        return error_response("City not found", 404)
    return jsonify({"message": "City updated"}), 200


@app.route('/api/cities/<id>', methods=['DELETE'])
def delete_city(id):
    result = db.cities.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return error_response("City not found", 404)
    return jsonify({"message": "City deleted"}), 200


# Default route for 404
@app.errorhandler(404)
def not_found(e):
    return error_response("The requested URL was not found on the server", 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
