import unittest
import requests

COUNTRIES_URL = "http://localhost:5001/api/countries"

class TestCountriesAPI(unittest.TestCase):
    def setUp(self):
        # Clear all countries
        clear_response = requests.delete(f"{COUNTRIES_URL}/clear")
        self.assertEqual(clear_response.status_code, 200, "Failed to clear countries")

        # Add a base test country
        payload = {"nume": "Romania", "lat": 45.9432, "lon": 24.9668}
        response = requests.post(COUNTRIES_URL, json=payload)
        self.assertEqual(response.status_code, 201, f"Failed to set up test country: {response.json()}")
        self.base_country_id = response.json()["id"]

        # Add a second test country
        payload = {"nume": "United States", "lat": 37.0902, "lon": -95.7129}
        response = requests.post(COUNTRIES_URL, json=payload)
        self.assertEqual(response.status_code, 201, f"Failed to set up test country: {response.json()}")
        self.second_country_id = response.json()["id"]

    def tearDown(self):
        # Separate test cases with a line
        print("-------------------------------------------------")

    def test_clear_countries(self):
        # Test clearing all countries
        response = requests.delete(f"{COUNTRIES_URL}/clear")
        self.assertEqual(response.status_code, 200, "Failed to clear countries")
        print(f"DELETE /countries/clear SUCCESS: {response.json()}")
        print("PASSED")

    def test_post_country_success(self):
        # Test adding a new country (201 Success Case)
        payload = {"nume": "Bulgaria", "lat": 42.7339, "lon": 25.4858}
        response = requests.post(COUNTRIES_URL, json=payload)
        self.assertEqual(response.status_code, 201, "Failed to add new country")
        print(f"POST /countries SUCCESS: {response.json()}")
        print("PASSED")

    def test_post_country_missing_fields(self):
        # Test adding a country with missing fields (400 Fail Case)
        payload = {"nume": "Missing Fields Country"}
        response = requests.post(COUNTRIES_URL, json=payload)
        self.assertEqual(response.status_code, 400, "Missing fields not handled")
        print(f"POST /countries FAIL (Missing Fields): {response.json()}")
        print("PASSED")

    def test_post_country_duplicate(self):
        # Test adding a duplicate country (409 Fail Case)
        payload = {"nume": "Romania", "lat": 45.9432, "lon": 24.9668}
        response = requests.post(COUNTRIES_URL, json=payload)
        self.assertEqual(response.status_code, 409, "Duplicate country not handled")
        print(f"POST /countries FAIL (Duplicate): {response.json()}")
        print("PASSED")

    def test_get_countries(self):
        # Test retrieving all countries. Should be the 2 test countries
        response = requests.get(COUNTRIES_URL)
        self.assertEqual(response.status_code, 200, "Failed to retrieve countries")
        print(f"GET /countries SUCCESS: {response.json()}")
        print("PASSED")

    def test_put_country_success(self):
        # Test updating the base test country (200 Success Case)
        update_payload = {"nume": "Romania Updated", "lat": 46.0, "lon": 25.0}
        response = requests.put(f"{COUNTRIES_URL}/{self.base_country_id}", json=update_payload)
        self.assertEqual(response.status_code, 200, "Failed to update base country")
        print(f"PUT /countries/{self.base_country_id} SUCCESS: {response.json()}")
        print("PASSED")

    def test_put_country_not_found(self):
        # Test updating a non-existent country (404 Fail Case)
        payload = {"nume": "Nonexistent Country", "lat": 0.0, "lon": 0.0}
        response = requests.put(f"{COUNTRIES_URL}/123456789101112131415167", json=payload)

        self.assertEqual(response.status_code, 404, "Non-existent country not handled")
        print(f"PUT /countries/123456789101112131415167 FAIL: {response.json()}")
        print("PASSED")

    def test_put_country_missing_fields(self):
        # Test updating a country with missing fields (400 Fail Case)
        payload = {"nume": "Missing Fields Country"}
        response = requests.put(f"{COUNTRIES_URL}/{self.base_country_id}", json=payload)
        self.assertEqual(response.status_code, 400, "Missing fields not handled")
        print(f"PUT /countries/{self.base_country_id} FAIL (Missing Fields): {response.json()}")
        print("PASSED")
    
    def test_put_country_bad_id(self):
        # Test updating a country with a bad ID (400 Fail Case)
        payload = {"nume": "Bad ID Country", "lat": 0.0, "lon": 0.0}
        response = requests.put(f"{COUNTRIES_URL}/bad_id", json=payload)
        self.assertEqual(response.status_code, 400, "Bad ID not handled")
        print(f"PUT /countries/bad_id FAIL: {response.json()}")
        print("PASSED")

    def test_delete_country_success(self):
        # Test deleting the base test country (200 Success Case)
        response = requests.delete(f"{COUNTRIES_URL}/{self.base_country_id}")
        self.assertEqual(response.status_code, 200, "Failed to delete base country")
        print(f"DELETE /countries/{self.base_country_id} SUCCESS: {response.json()}")
        print("PASSED")

    def test_delete_country_not_found(self):
        # Test deleting a non-existent country (404 Fail Case)
        response = requests.delete(f"{COUNTRIES_URL}/123456789101112131415167")
        self.assertEqual(response.status_code, 404, "Non-existent country not handled")
        print(f"DELETE /countries/123456789101112131415167 FAIL: {response.json()}")
        print("PASSED")

    def test_delete_country_bad_id(self):
        # Test deleting a country with a bad ID (400 Fail Case)
        response = requests.delete(f"{COUNTRIES_URL}/bad_id")
        self.assertEqual(response.status_code, 404, "Bad ID meaning country not found not handled")
        print(f"DELETE /countries/bad_id FAIL: {response.json()}")
        print("PASSED")

    def test_delete_country_with_cities_with_temperatures(self):
        # Test deleting a country with cities that have temperatures
        # Add a base test city
        CITIES_URL = "http://localhost:5001/api/cities"
        payload = {"idTara": self.base_country_id, "nume": "Bucharest", "lat": 44.4268, "lon": 26.1025}
        response = requests.post(CITIES_URL, json=payload)
        self.assertEqual(response.status_code, 201, f"Failed to set up test city: {response.json()}")
        base_city_id = response.json()["id"]

        # Add a temperature for the base city
        TEMPERATURES_URL = "http://localhost:5001/api/temperatures"
        payload = {"idOras": base_city_id, "valoare": 25.0, "timestamp": "2021-01-01T00:00:00Z"}
        response = requests.post(TEMPERATURES_URL, json=payload)
        self.assertEqual(response.status_code, 201, f"Failed to set up test temperature: {response.json()}")

        # Test deleting the country
        response = requests.delete(f"{COUNTRIES_URL}/{self.base_country_id}")
        self.assertEqual(response.status_code, 200, "Failed to delete country with cities with temperatures")

        # Assert that we dont have that city anymore
        response = requests.get(f"{CITIES_URL}/country/{self.base_country_id}")
        # Assert that response is country not found
        self.assertEqual(response.json(), {"error": "Country not found"}, "Country not deleted")

        # Assert that we dont have that temperature anymore
        response = requests.get(f"{TEMPERATURES_URL}/cities/{base_city_id}")
        # Assert that our temperature is not in response
        self.assertNotIn(base_city_id, [temperature["id"] for temperature in response.json()], "Temperature not deleted")

        print(f"DELETE /countries/{self.base_country_id} SUCCESS: {response.json()}")
        print("PASSED")

if __name__ == "__main__":
    unittest.main()
