import unittest
import requests

COUNTRIES_URL = "http://localhost:5001/api/countries"

class TestCountriesAPI(unittest.TestCase):
    def setUp(self):
        # Clear all countries
        clear_response = requests.delete(f"{COUNTRIES_URL}/clear")
        self.assertEqual(clear_response.status_code, 200, "Failed to clear countries")

        # Add a base test country
        payload = {"nume_tara": "Romania", "latitudine": 45.9432, "longitudine": 24.9668}
        response = requests.post(COUNTRIES_URL, json=payload)
        self.assertEqual(response.status_code, 201, f"Failed to set up test country: {response.json()}")
        self.base_country_id = response.json()["id"]

        # Add a second test country
        payload = {"nume_tara": "United States", "latitudine": 37.0902, "longitudine": -95.7129}
        response = requests.post(COUNTRIES_URL, json=payload)
        self.assertEqual(response.status_code, 201, f"Failed to set up test country: {response.json()}")

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
        payload = {"nume_tara": "Bulgaria", "latitudine": 42.7339, "longitudine": 25.4858}
        response = requests.post(COUNTRIES_URL, json=payload)
        self.assertEqual(response.status_code, 201, "Failed to add new country")
        print(f"POST /countries SUCCESS: {response.json()}")
        print("PASSED")

    def test_post_country_missing_fields(self):
        # Test adding a country with missing fields (400 Fail Case)
        payload = {"nume_tara": "Missing Fields Country"}
        response = requests.post(COUNTRIES_URL, json=payload)
        self.assertEqual(response.status_code, 400, "Missing fields not handled")
        print(f"POST /countries FAIL (Missing Fields): {response.json()}")
        print("PASSED")

    def test_post_country_duplicate(self):
        # Test adding a duplicate country (409 Fail Case)
        payload = {"nume_tara": "Romania", "latitudine": 45.9432, "longitudine": 24.9668}
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
        update_payload = {"nume_tara": "Romania Updated", "latitudine": 46.0, "longitudine": 25.0}
        response = requests.put(f"{COUNTRIES_URL}/{self.base_country_id}", json=update_payload)
        self.assertEqual(response.status_code, 200, "Failed to update base country")
        print(f"PUT /countries/{self.base_country_id} SUCCESS: {response.json()}")
        print("PASSED")

    def test_put_country_not_found(self):
        # Test updating a non-existent country (404 Fail Case)
        payload = {"nume_tara": "Nonexistent Country", "latitudine": 0.0, "longitudine": 0.0}
        response = requests.put(f"{COUNTRIES_URL}/123456789101112131415167", json=payload)

        self.assertEqual(response.status_code, 404, "Non-existent country not handled")
        print(f"PUT /countries/123456789101112131415167 FAIL: {response.json()}")
        print("PASSED")

    def test_put_country_missing_fields(self):
        # Test updating a country with missing fields (400 Fail Case)
        payload = {"nume_tara": "Missing Fields Country"}
        response = requests.put(f"{COUNTRIES_URL}/{self.base_country_id}", json=payload)
        self.assertEqual(response.status_code, 400, "Missing fields not handled")
        print(f"PUT /countries/{self.base_country_id} FAIL (Missing Fields): {response.json()}")
        print("PASSED")
    
    def test_put_country_bad_id(self):
        # Test updating a country with a bad ID (400 Fail Case)
        payload = {"nume_tara": "Bad ID Country", "latitudine": 0.0, "longitudine": 0.0}
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
        self.assertEqual(response.status_code, 400, "Bad ID not handled")
        print(f"DELETE /countries/bad_id FAIL: {response.json()}")
        print("PASSED")

if __name__ == "__main__":
    unittest.main()
