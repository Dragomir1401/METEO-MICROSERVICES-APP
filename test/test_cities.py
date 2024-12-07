import unittest
import requests

BASE_URL_COUNTRIES = "http://localhost:5001/api/countries"
BASE_URL_CITIES = "http://localhost:5001/api/cities"

class TestCitiesAPI(unittest.TestCase):
    def setUp(self):
        # Clear countries and cities
        clear_countries_response = requests.delete(f"{BASE_URL_COUNTRIES}/clear")
        self.assertEqual(clear_countries_response.status_code, 200, "Failed to clear countries")

        clear_cities_response = requests.delete(f"{BASE_URL_CITIES}/clear")
        self.assertEqual(clear_cities_response.status_code, 200, "Failed to clear cities")

        # Create a base country for tests
        payload = {"nume": "Romania", "lat": 45.9432, "lon": 24.9668}
        response = requests.post(BASE_URL_COUNTRIES, json=payload)
        self.assertEqual(response.status_code, 201, f"Failed to create base test country: {response.json()}")
        self.base_country_id = response.json()["id"]

        # Add a base city for the base country
        payload = {"idTara": self.base_country_id, "nume": "Cluj-Napoca", "lat": 46.7712, "lon": 23.6236}
        response = requests.post(BASE_URL_CITIES, json=payload)
        self.assertEqual(response.status_code, 201, f"Failed to create base test city: {response.json()}")
        self.base_city_id = response.json()["id"]

        # Add a secondary city for the base country
        payload = {"idTara": self.base_country_id, "nume": "Brasov", "lat": 45.6579, "lon": 25.6012}
        response = requests.post(BASE_URL_CITIES, json=payload)
        self.assertEqual(response.status_code, 201, f"Failed to create secondary test city: {response.json()}")
        self.secondary_city_id = response.json()["id"]

    def tearDown(self):
        # Separate test cases with a line
        print("-------------------------------------------------")

    def test_post_city_success(self):
        # Test adding a city (201 Success Case)
        payload = {"idTara": self.base_country_id, "nume": "Bucharest", "lat": 44.4268, "lon": 26.1025}
        response = requests.post(BASE_URL_CITIES, json=payload)
        self.assertEqual(response.status_code, 201, "Failed to add city (Success Case)")
        print(f"POST /cities SUCCESS: {response.json()}")
        print("PASSED")

    def test_post_city_invalid_country(self):
        # Test adding a city with an invalid country ID (400 Fail Case)
        payload = {"idTara": "123456789101112131415167", "nume": "Invalid City", "lat": 0.0, "lon": 0.0}
        response = requests.post(BASE_URL_CITIES, json=payload)
        self.assertEqual(response.status_code, 404, "Invalid country ID not handled")
        print(f"POST /cities FAIL (Invalid Country): {response.json()}")
        print("PASSED")

    def test_post_city_missing_fields(self):
        # Test adding a city with missing fields (400 Fail Case)
        payload = {"idTara": self.base_country_id, "nume": "Missing Fields City"}
        response = requests.post(BASE_URL_CITIES, json=payload)
        self.assertEqual(response.status_code, 400, "Missing fields not handled")
        print(f"POST /cities FAIL (Missing Fields): {response.json()}")
        print("PASSED")

    def test_post_city_duplicate(self):
        # Test adding a duplicate city (409 Fail Case)
        payload = {"idTara": self.base_country_id, "nume": "Cluj-Napoca", "lat": 46.7712, "lon": 23.6236}
        requests.post(BASE_URL_CITIES, json=payload)

        response = requests.post(BASE_URL_CITIES, json=payload)
        self.assertEqual(response.status_code, 409, "Duplicate city not handled")
        print(f"POST /cities FAIL (Duplicate): {response.json()}")
        print("PASSED")

    def test_post_city_bad_country_id(self):
        # Test adding a city with a bad country ID (400 Fail Case)
        payload = {"idTara": "0000", "nume": "Bad Country City", "lat": 0.0, "lon": 0.0}
        response = requests.post(BASE_URL_CITIES, json=payload)
        self.assertEqual(response.status_code, 400, "Bad country ID not handled")
        print(f"POST /cities FAIL (Bad Country ID): {response.json()}")
        print("PASSED")

    def test_get_cities(self):
        # Test retrieving all cities. Should be the 2 test cities
        response = requests.get(BASE_URL_CITIES)
        self.assertEqual(response.status_code, 200, "Failed to retrieve cities")
        print(f"GET /cities SUCCESS: {response.json()}")
        print("PASSED")

    def test_put_city_success(self):
        # Test updating the base test city (200 Success Case)
        update_payload = {"idTara": self.base_country_id, "nume": "Cluj-Napoca Updated", "lat": 47.0, "lon": 24.0}
        response = requests.put(f"{BASE_URL_CITIES}/{self.base_city_id}", json=update_payload)
        self.assertEqual(response.status_code, 200, "Failed to update base city")
        print(f"PUT /cities/{self.base_city_id} SUCCESS: {response.json()}")
        print("PASSED")

    def test_put_city_not_found(self):
        # Test updating a non-existent city (404 Fail Case)
        payload = {"id": self.base_city_id, "idTara": self.base_country_id, "nume": "Nonexistent City", "lat": 0.0, "lon": 0.0}
        response = requests.put(f"{BASE_URL_CITIES}/123456789101112131415167", json=payload)
        self.assertEqual(response.status_code, 404, "Non-existent city not handled")
        print(f"PUT /cities/123456789101112131415167 FAIL: {response.json()}")
        print("PASSED")

    def test_put_city_country_not_found(self):
        # Test updating a city with a non-existent country (404 Fail Case)
        payload = {"id": self.base_city_id, "idTara": "123456789101112131415167", "nume": "Nonexistent Country City", "lat": 0.0, "lon": 0.0}
        response = requests.put(f"{BASE_URL_CITIES}/{self.base_city_id}", json=payload)
        self.assertEqual(response.status_code, 404, "Non-existent country not handled")
        print(f"PUT /cities/{self.base_city_id} FAIL (Non-existent Country): {response.json()}")
        print("PASSED")

    def test_put_city_missing_fields(self):
        # Test updating a city with missing fields (400 Fail Case)
        payload = {"idTara": self.base_country_id, "nume": "Missing Fields City"}
        response = requests.put(f"{BASE_URL_CITIES}/{self.base_city_id}", json=payload)
        self.assertEqual(response.status_code, 400, "Missing fields not handled")
        print(f"PUT /cities/{self.base_city_id} FAIL (Missing Fields): {response.json()}")
        print("PASSED")

    def test_put_city_bad_name(self):
        # Test updating a city with a bad ID (400 Fail Case)
        payload = {"id": self.base_city_id, "idTara": self.base_country_id, "nume": "Bad ID City", "lat": 0.0, "lon": 0.0}
        response = requests.put(f"{BASE_URL_CITIES}/bad_id", json=payload)
        self.assertEqual(response.status_code, 400, "Bad ID not handled")
        print(f"PUT /cities/bad_id FAIL: {response.json()}")
        print("PASSED")

    def test_put_cities_bad_id(self):
        # Test updating a city with a bad ID (400 Fail Case)
        payload = {"id": "bad_id", "idTara": self.base_country_id, "nume": "Bad ID City", "lat": 0.0, "lon": 0.0}
        response = requests.put(f"{BASE_URL_CITIES}/{self.base_city_id}", json=payload)
        self.assertEqual(response.status_code, 400, "Bad ID not handled")
        print(f"PUT /cities/{self.base_city_id} FAIL (Bad ID): {response.json()}")
        print("PASSED")

    def test_get_cities_by_country_success(self):
        # Test retrieving cities by country. Should be the 2 test cities
        response = requests.get(f"{BASE_URL_CITIES}/country/{self.base_country_id}")
        self.assertEqual(response.status_code, 200, "Failed to retrieve cities by country")
        print(f"GET /cities/country/{self.base_country_id} SUCCESS: {response.json()}")
        print("PASSED")

    def test_get_cities_by_country_invalid_id(self):
        # Test retrieving cities by an invalid country ID (400 Fail Case)
        response = requests.get(f"{BASE_URL_CITIES}/country/0000")
        self.assertEqual(response.status_code, 400, "Invalid country ID not handled")
        print(f"GET /cities/country/0000 FAIL: {response.json()}")
        print("PASSED")

    def test_get_cities_by_country_not_found(self):
        # Test retrieving cities by a non-existent country ID (404 Fail Case)
        response = requests.get(f"{BASE_URL_CITIES}/country/123456789101112131415167")
        self.assertEqual(response.status_code, 404, "Non-existent country not handled")
        print(f"GET /cities/country/123456789101112131415167 FAIL: {response.json()}")
        print("PASSED")

    def test_delete_city_success(self):
        # Test deleting a city (200 Success Case)
        response = requests.delete(f"{BASE_URL_CITIES}/{self.base_city_id}")
        self.assertEqual(response.status_code, 200, "Failed to delete city")
        print(f"DELETE /cities/{self.base_city_id} SUCCESS: {response.json()}")
        print("PASSED")

    def test_delete_city_not_found(self):
        # Test deleting a non-existent city (404 Fail Case)
        response = requests.delete(f"{BASE_URL_CITIES}/123456789101112131415167")
        self.assertEqual(response.status_code, 404, "Non-existent city not handled")
        print(f"DELETE /cities/123456789101112131415167 FAIL: {response.json()}")
        print("PASSED")

    def test_delete_city_bad_id(self):
        # Test deleting a city with a bad ID (400 Fail Case)
        response = requests.delete(f"{BASE_URL_CITIES}/bad_id")
        self.assertEqual(response.status_code, 404, "Bad ID meaning non existing city not handled")
        print(f"DELETE /cities/bad_id FAIL: {response.json()}")
        print("PASSED")

    def test_delete_city_with_temperatures(self):
        # Add some temperatures for the secondary city
        payload = {"idOras": self.secondary_city_id, "valoare": 25.0, "timestamp": "2021-01-01T00:00:00"}
        response = requests.post("http://localhost:5001/api/temperatures", json=payload)
        self.assertEqual(response.status_code, 201, f"Failed to set up test temperature: {response.json()}")
        temperature_id = response.json()["id"]

        # Delete the city with temperatures
        response = requests.delete(f"{BASE_URL_CITIES}/{self.secondary_city_id}")
        self.assertEqual(response.status_code, 200, "Failed to delete city with temperatures")
        print(f"DELETE /cities/{self.secondary_city_id} SUCCESS: {response.json()}")

        # Check if the temperature was deleted
        TEMPERATURES_URL = "http://localhost:5001/api/temperatures"
        response = requests.get(f"{TEMPERATURES_URL}/cities/{self.base_city_id}")
        self.assertNotIn(temperature_id, [temperature["id"] for temperature in response.json()], "Temperature not deleted")

        print("PASSED")


if __name__ == "__main__":
    unittest.main()
