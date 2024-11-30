import unittest
import requests

BASE_URL_TEMPERATURES = "http://localhost:5001/api/temperatures"
BASE_URL_COUNTRIES = "http://localhost:5001/api/countries"
BASE_URL_CITIES = "http://localhost:5001/api/cities"

class TestTemperaturesAPI(unittest.TestCase):
    def setUp(self):
        """Clear the database and set up test data"""
        # Clear all temperatures
        requests.delete(f"{BASE_URL_TEMPERATURES}/clear")
        
        # Add a test country
        self.country_payload = {"nume_tara": "Romania", "latitudine": 45.9432, "longitudine": 24.9668}
        country_response = requests.post(BASE_URL_COUNTRIES, json=self.country_payload)

        try:
            self.assertEqual(country_response.status_code, 201, f"Failed to add test country: {country_response.text}")
            self.country_id = country_response.json()["id"]
        except KeyError:
            print(f"Unexpected country response: {country_response.json()}")
            raise

        # Add a test city
        self.city_payload = {"id_tara": self.country_id, "nume_oras": "Bucharest", "latitudine": 44.4268, "longitudine": 26.1025}
        city_response = requests.post(BASE_URL_CITIES, json=self.city_payload)
        try:
            self.assertEqual(city_response.status_code, 201, f"Failed to add test city: {city_response.text}")
            self.city_id = city_response.json()["id"]
        except KeyError:
            print(f"Unexpected city response: {city_response.json()}")
            raise


    def test_post_temperature_success(self):
        """Test adding a temperature (Success Case)"""
        payload = {"id_oras": self.city_id, "valoare": 25.0}
        response = requests.post(BASE_URL_TEMPERATURES, json=payload)
        self.assertEqual(response.status_code, 201, "Failed to add temperature")
        print(f"POST /temperatures SUCCESS: {response.json()}")

    def test_post_temperature_invalid_city(self):
        """Test adding a temperature with an invalid city ID (Fail Case)"""
        payload = {"id_oras": "000000000000000000000000", "valoare": 30.0}
        response = requests.post(BASE_URL_TEMPERATURES, json=payload)
        self.assertEqual(response.status_code, 404, "Invalid city ID not handled")
        print(f"POST /temperatures FAIL (Invalid City): {response.json()}")

    def test_get_country_temperatures(self):
        """Test retrieving temperatures for a specific country"""
        # Add a temperature
        temp_payload = {"id_oras": self.city_id, "valoare": 22.5}
        temp_response = requests.post(BASE_URL_TEMPERATURES, json=temp_payload)
        self.assertEqual(temp_response.status_code, 201, f"Failed to add temperature: {temp_response.json()}")

        # Retrieve temperatures by country
        response = requests.get(f"{BASE_URL_TEMPERATURES}/countries/{self.country_id}")
        self.assertEqual(response.status_code, 200, "Failed to retrieve country temperatures")
        print(f"GET /temperatures/countries/{self.country_id} SUCCESS: {response.json()}")

    def test_put_temperature_success(self):
        """Test updating a temperature (Success Case)"""
        # Add a temperature
        temp_payload = {"id_oras": self.city_id, "valoare": 20.0}
        temp_response = requests.post(BASE_URL_TEMPERATURES, json=temp_payload)
        self.assertEqual(temp_response.status_code, 201, f"Failed to add temperature: {temp_response.json()}")
        temp_id = temp_response.json()["id"]

        # Update the temperature
        update_payload = {"id_oras": self.city_id, "valoare": 25.0}
        response = requests.put(f"{BASE_URL_TEMPERATURES}/{temp_id}", json=update_payload)
        self.assertEqual(response.status_code, 200, "Failed to update temperature")
        print(f"PUT /temperatures/{temp_id} SUCCESS: {response.json()}")

    def test_put_temperature_not_found(self):
        """Test updating a non-existent temperature (Fail Case)"""
        payload = {"id_oras": "000000000000000000000000", "valoare": 25.0}
        response = requests.put(f"{BASE_URL_TEMPERATURES}/000000000000000000000000", json=payload)

        self.assertEqual(response.status_code, 404, "Non-existent temperature not handled")
        try:
            print(f"PUT /temperatures/000000000000000000000000 FAIL: {response.json()}")
        except requests.exceptions.JSONDecodeError:
            print(f"PUT /temperatures/000000000000000000000000 FAIL: {response.text}")

if __name__ == "__main__":
    unittest.main()
