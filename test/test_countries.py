import unittest
import requests

BASE_URL = "http://localhost:5001/api/countries"

class TestCountriesAPI(unittest.TestCase):
    def setUp(self):
        """Clear the database and add a base test country before each test"""
        # Clear all countries
        clear_response = requests.delete(f"{BASE_URL}/clear")
        self.assertEqual(clear_response.status_code, 200, "Failed to clear countries")

        # Add a base test country
        payload = {"nume_tara": "Romania", "latitudine": 45.9432, "longitudine": 24.9668}
        response = requests.post(BASE_URL, json=payload)
        self.assertEqual(response.status_code, 201, f"Failed to set up test country: {response.json()}")
        self.base_country_id = response.json()["id"]

    def test_post_country_success(self):
        """Test adding a new country (Success Case)"""
        payload = {"nume_tara": "Bulgaria", "latitudine": 42.7339, "longitudine": 25.4858}
        response = requests.post(BASE_URL, json=payload)
        self.assertEqual(response.status_code, 201, "Failed to add new country")
        print(f"POST /countries SUCCESS: {response.json()}")

    def test_post_country_duplicate(self):
        """Test adding a duplicate country (Fail Case)"""
        payload = {"nume_tara": "Romania", "latitudine": 45.9432, "longitudine": 24.9668}
        response = requests.post(BASE_URL, json=payload)
        self.assertEqual(response.status_code, 409, "Duplicate country not handled")
        print(f"POST /countries FAIL (Duplicate): {response.json()}")

    def test_get_countries(self):
        """Test retrieving all countries"""
        response = requests.get(BASE_URL)
        self.assertEqual(response.status_code, 200, "Failed to retrieve countries")
        print(f"GET /countries SUCCESS: {response.json()}")

    def test_put_country_success(self):
        """Test updating the base test country (Success Case)"""
        update_payload = {"nume_tara": "Romania Updated", "latitudine": 46.0, "longitudine": 25.0}
        response = requests.put(f"{BASE_URL}/{self.base_country_id}", json=update_payload)
        self.assertEqual(response.status_code, 200, "Failed to update base country")
        print(f"PUT /countries/{self.base_country_id} SUCCESS: {response.json()}")

    def test_put_country_not_found(self):
        """Test updating a non-existent country (Fail Case)"""
        payload = {"nume_tara": "Nonexistent Country", "latitudine": 0.0, "longitudine": 0.0}
        response = requests.put(f"{BASE_URL}/000000000000000000000000", json=payload)
        self.assertEqual(response.status_code, 404, "Non-existent country not handled")
        print(f"PUT /countries/000000000000000000000000 FAIL: {response.json()}")

    def test_delete_country_success(self):
        """Test deleting the base test country (Success Case)"""
        response = requests.delete(f"{BASE_URL}/{self.base_country_id}")
        self.assertEqual(response.status_code, 200, "Failed to delete base country")
        print(f"DELETE /countries/{self.base_country_id} SUCCESS: {response.json()}")

    def test_delete_country_not_found(self):
        """Test deleting a non-existent country (Fail Case)"""
        response = requests.delete(f"{BASE_URL}/000000000000000000000000")
        self.assertEqual(response.status_code, 404, "Non-existent country not handled")
        print(f"DELETE /countries/000000000000000000000000 FAIL: {response.json()}")

if __name__ == "__main__":
    unittest.main()
