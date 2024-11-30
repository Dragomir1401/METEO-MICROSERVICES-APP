import unittest
import requests

BASE_URL = "http://localhost:5001/api/countries"

class TestCountriesAPI(unittest.TestCase):
    def setUp(self):
        """Clear the database and add a base test country before each test"""
        # Clear all countries
        requests.delete(f"{BASE_URL}/clear")
        
        # Add a base test country
        payload = {"nume": "Romania", "lat": 45.9432, "lon": 24.9668}
        response = requests.post(BASE_URL, json=payload)
        self.assertEqual(response.status_code, 201, "Failed to set up test country")
        self.base_country_id = response.json()["id"]

    def test_post_country_success(self):
        """Test adding a new country (Success Case)"""
        payload = {"nume": "Bulgaria", "lat": 42.7339, "lon": 25.4858}
        response = requests.post(BASE_URL, json=payload)
        self.assertEqual(response.status_code, 201, "Failed to add new country")
        print(f"POST /countries SUCCESS: {response.json()}")

    def test_post_country_duplicate(self):
        """Test adding a duplicate country (Fail Case)"""
        payload = {"nume": "Romania", "lat": 45.9432, "lon": 24.9668}
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
        update_payload = {"nume": "Romania Updated", "lat": 46.0, "lon": 25.0}
        response = requests.put(f"{BASE_URL}/{self.base_country_id}", json=update_payload)
        self.assertEqual(response.status_code, 200, "Failed to update base country")
        print(f"PUT /countries/{self.base_country_id} SUCCESS: {response.json()}")

    def test_put_country_not_found(self):
        """Test updating a non-existent country (Fail Case)"""
        payload = {"nume": "Nonexistent Country", "lat": 0.0, "lon": 0.0}
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
