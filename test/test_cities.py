import unittest
import requests

BASE_URL_COUNTRIES = "http://localhost:5001/api/countries"
BASE_URL_CITIES = "http://localhost:5001/api/cities"

class TestCitiesAPI(unittest.TestCase):
    def setUp(self):
        """Clear the database before each test and create a test country"""
        # Clear countries and cities
        requests.delete(f"{BASE_URL_COUNTRIES}/clear")
        requests.delete(f"{BASE_URL_CITIES}/clear")

        # Create a test country
        payload = {"nume": "Romania", "lat": 45.9432, "lon": 24.9668}
        response = requests.post(BASE_URL_COUNTRIES, json=payload)
        self.country_id = response.json()["id"]

    def test_post_city_success(self):
        """Test adding a city (Success Case)"""
        payload = {"idTara": self.country_id, "nume": "Bucharest", "lat": 44.4268, "lon": 26.1025}
        response = requests.post(BASE_URL_CITIES, json=payload)
        self.assertEqual(response.status_code, 201, "Failed to add city (Success Case)")
        print(f"POST /cities SUCCESS: {response.json()}")

    def test_post_city_invalid_country(self):
        """Test adding a city with an invalid country ID (Fail Case)"""
        payload = {"idTara": "000000000000000000000000", "nume": "Invalid City", "lat": 0.0, "lon": 0.0}
        response = requests.post(BASE_URL_CITIES, json=payload)
        self.assertEqual(response.status_code, 404, "Invalid country ID not handled")
        print(f"POST /cities FAIL (Invalid Country): {response.json()}")

    def test_get_cities(self):
        """Test retrieving all cities"""
        # Add a city
        payload = {"idTara": self.country_id, "nume": "Cluj-Napoca", "lat": 46.7712, "lon": 23.6236}
        requests.post(BASE_URL_CITIES, json=payload)

        response = requests.get(BASE_URL_CITIES)
        self.assertEqual(response.status_code, 200, "Failed to retrieve cities")
        print(f"GET /cities SUCCESS: {response.json()}")

    def test_get_cities_by_country(self):
        """Test retrieving cities by country"""
        # Add a city
        payload = {"idTara": self.country_id, "nume": "Timisoara", "lat": 45.7489, "lon": 21.2087}
        requests.post(BASE_URL_CITIES, json=payload)

        response = requests.get(f"{BASE_URL_CITIES}/country/{self.country_id}")
        self.assertEqual(response.status_code, 200, "Failed to retrieve cities by country")
        print(f"GET /cities/country/{self.country_id} SUCCESS: {response.json()}")

    def test_delete_city_success(self):
        """Test deleting a city (Success Case)"""
        # Add a city
        payload = {"idTara": self.country_id, "nume": "Sibiu", "lat": 45.7983, "lon": 24.1256}
        add_response = requests.post(BASE_URL_CITIES, json=payload)
        city_id = add_response.json()["id"]

        # Delete the city
        response = requests.delete(f"{BASE_URL_CITIES}/{city_id}")
        self.assertEqual(response.status_code, 200, "Failed to delete city")
        print(f"DELETE /cities/{city_id} SUCCESS: {response.json()}")

    def test_delete_city_not_found(self):
        """Test deleting a non-existent city (Fail Case)"""
        response = requests.delete(f"{BASE_URL_CITIES}/000000000000000000000000")
        self.assertEqual(response.status_code, 404, "Non-existent city not handled")
        print(f"DELETE /cities/000000000000000000000000 FAIL: {response.json()}")

if __name__ == "__main__":
    unittest.main()
