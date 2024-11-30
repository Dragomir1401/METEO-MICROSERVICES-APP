import unittest
import requests

BASE_URL_COUNTRIES = "http://localhost:5001/api/countries"
BASE_URL_CITIES = "http://localhost:5001/api/cities"

class TestCitiesAPI(unittest.TestCase):
    def setUp(self):
        """Clear the database before each test"""
        # Clear countries and cities
        clear_countries_response = requests.delete(f"{BASE_URL_COUNTRIES}/clear")
        self.assertEqual(clear_countries_response.status_code, 200, "Failed to clear countries")

        clear_cities_response = requests.delete(f"{BASE_URL_CITIES}/clear")
        self.assertEqual(clear_cities_response.status_code, 200, "Failed to clear cities")

        # Create a base country for tests
        payload = {"nume_tara": "Romania", "latitudine": 45.9432, "longitudine": 24.9668}
        response = requests.post(BASE_URL_COUNTRIES, json=payload)
        self.assertEqual(response.status_code, 201, f"Failed to create base test country: {response.json()}")
        self.base_country_id = response.json()["id"]

    def test_post_city_success(self):
        """Test adding a city (Success Case)"""
        payload = {"id_tara": self.base_country_id, "nume_oras": "Bucharest", "latitudine": 44.4268, "longitudine": 26.1025}
        response = requests.post(BASE_URL_CITIES, json=payload)
        self.assertEqual(response.status_code, 201, "Failed to add city (Success Case)")
        print(f"POST /cities SUCCESS: {response.json()}")

    def test_post_city_invalid_country(self):
        """Test adding a city with an invalid country ID (Fail Case)"""
        payload = {"id_tara": "000000000000000000000000", "nume_oras": "Invalid City", "latitudine": 0.0, "longitudine": 0.0}
        response = requests.post(BASE_URL_CITIES, json=payload)
        self.assertEqual(response.status_code, 404, "Invalid country ID not handled")
        print(f"POST /cities FAIL (Invalid Country): {response.json()}")

    def test_get_cities(self):
        """Test retrieving all cities"""
        # Add a city
        payload = {"id_tara": self.base_country_id, "nume_oras": "Cluj-Napoca", "latitudine": 46.7712, "longitudine": 23.6236}
        requests.post(BASE_URL_CITIES, json=payload)

        response = requests.get(BASE_URL_CITIES)
        self.assertEqual(response.status_code, 200, "Failed to retrieve cities")
        print(f"GET /cities SUCCESS: {response.json()}")

    def test_get_cities_by_country(self):
        """Test retrieving cities by country"""
        # Use the country created in setUp
        country_id = self.base_country_id

        # Add a city to the existing country
        city_payload = {"id_tara": country_id, "nume_oras": "Timisoara", "latitudine": 45.7489, "longitudine": 21.2087}
        city_response = requests.post(BASE_URL_CITIES, json=city_payload)
        self.assertEqual(city_response.status_code, 201, f"Failed to add city: {city_response.json()}")

        # Test retrieval of cities by country
        response = requests.get(f"{BASE_URL_CITIES}/country/{country_id}")
        self.assertEqual(response.status_code, 200, "Failed to retrieve cities by country")
        print(f"GET /cities/country/{country_id} SUCCESS: {response.json()}")

    def test_delete_city_success(self):
        """Test deleting a city (Success Case)"""
        # Add a city
        payload = {"id_tara": self.base_country_id, "nume_oras": "Sibiu", "latitudine": 45.7983, "longitudine": 24.1256}
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
