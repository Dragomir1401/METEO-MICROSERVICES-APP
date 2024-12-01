import unittest
import requests

BASE_URL_TEMPERATURES = "http://localhost:5001/api/temperatures"
BASE_URL_COUNTRIES = "http://localhost:5001/api/countries"
BASE_URL_CITIES = "http://localhost:5001/api/cities"

class TestTemperaturesAPI(unittest.TestCase):
    def setUp(self):
        # Clear all temperatures, countries, and cities
        clear_temperatures_response = requests.delete(f"{BASE_URL_TEMPERATURES}/clear")
        self.assertEqual(clear_temperatures_response.status_code, 200, "Failed to clear temperatures")
        clear_countries_response = requests.delete(f"{BASE_URL_COUNTRIES}/clear")
        self.assertEqual(clear_countries_response.status_code, 200, "Failed to clear countries")
        clear_cities_response = requests.delete(f"{BASE_URL_CITIES}/clear")
        self.assertEqual(clear_cities_response.status_code, 200, "Failed to clear cities")

        # Add a base country for test
        payload = {"nume_tara": "Romania", "latitudine": 45.9432, "longitudine": 24.9668}
        response = requests.post(BASE_URL_COUNTRIES, json=payload)
        self.assertEqual(response.status_code, 201, f"Failed to add test country: {response.text}")
        self.base_country_id = response.json()["id"]

        # Add a base city for the base country
        payload = {"id_tara": self.base_country_id, "nume_oras": "Cluj-Napoca", "latitudine": 46.7712, "longitudine": 23.6236}
        response = requests.post(BASE_URL_CITIES, json=payload)
        self.assertEqual(response.status_code, 201, f"Failed to add test city: {response.text}")
        self.base_city_id = response.json()["id"]

        # Add a second city for the base country
        payload = {"id_tara": self.base_country_id, "nume_oras": "Brasov", "latitudine": 45.6579, "longitudine": 25.6012}
        response = requests.post(BASE_URL_CITIES, json=payload)
        self.assertEqual(response.status_code, 201, f"Failed to add test city: {response.text}")
        self.secondary_city_id = response.json()["id"]

        # Add a temperature for the base city
        temp_payload = {"id_oras": self.base_city_id, "valoare": 22.5}
        temp_response = requests.post(BASE_URL_TEMPERATURES, json=temp_payload)
        self.assertEqual(temp_response.status_code, 201, f"Failed to add test temperature: {temp_response.text}")

        # Add a secondary temperature for the base city
        temp_payload = {"id_oras": self.base_city_id, "valoare": 23.0}
        temp_response = requests.post(BASE_URL_TEMPERATURES, json=temp_payload)
        self.assertEqual(temp_response.status_code, 201, f"Failed to add test temperature: {temp_response.text}")

        # Add a temperature for the secondary city
        temp_payload = {"id_oras": self.secondary_city_id, "valoare": 24.0}
        temp_response = requests.post(BASE_URL_TEMPERATURES, json=temp_payload)
        self.assertEqual(temp_response.status_code, 201, f"Failed to add test temperature: {temp_response.text}")

        # Add a secondary temperature for the secondary city
        temp_payload = {"id_oras": self.secondary_city_id, "valoare": 25.0}
        temp_response = requests.post(BASE_URL_TEMPERATURES, json=temp_payload)
        self.assertEqual(temp_response.status_code, 201, f"Failed to add test temperature: {temp_response.text}")

    def tearDown(self):
        # Separate test cases with a line
        print("-------------------------------------------------")

    # def test_clear_temperatures(self):
    #     """Test clearing all temperatures"""
    #     response = requests.delete(f"{BASE_URL_TEMPERATURES}/clear")
    #     self.assertEqual(response.status_code, 200, "Failed to clear temperatures")
    #     print(f"DELETE /temperatures/clear SUCCESS: {response.json()}")
    #     print("PASSED")

    # def test_post_temperature_success(self):
    #     # Test adding a temperature (201 Success Case)
    #     payload = {"id_oras": self.base_city_id, "valoare": 25.0}
    #     response = requests.post(BASE_URL_TEMPERATURES, json=payload)
    #     self.assertEqual(response.status_code, 201, "Failed to add temperature")
    #     print(f"POST /temperatures SUCCESS: {response.json()}")
    #     print("PASSED")

    # def test_post_temperature_missing_fields(self):
    #     # Test adding a temperature with missing fields (400 Fail Case)
    #     payload = {"id_oras": self.base_city_id}
    #     response = requests.post(BASE_URL_TEMPERATURES, json=payload)
    #     self.assertEqual(response.status_code, 400, "Missing fields not handled")
    #     print(f"POST /temperatures FAIL (Missing Fields): {response.json()}")
    #     print("PASSED")

    # def test_post_temperature_invalid_city(self):
    #     # Test adding a temperature with an invalid city ID (404 Fail Case)
    #     payload = {"id_oras": "123456789101112131415167", "valoare": 30.0}
    #     response = requests.post(BASE_URL_TEMPERATURES, json=payload)
    #     self.assertEqual(response.status_code, 404, "Invalid city ID not handled")
    #     print(f"POST /temperatures FAIL (Invalid City): {response.json()}")
    #     print("PASSED")

    # def test_post_temperature_bad_id(self):
    #     # Test adding a temperature with a bad city ID (400 Fail Case)
    #     payload = {"id_oras": "bad_id", "valoare": 30.0}
    #     response = requests.post(BASE_URL_TEMPERATURES, json=payload)
    #     self.assertEqual(response.status_code, 400, "Bad city ID not handled")
    #     print(f"POST /temperatures FAIL (Bad ID): {response.json()}")
    #     print("PASSED")

    # Cannot test timestamp uniqueness due to the nature of the test and using utcnow() to set the timestamp

    # def test_get_temperatures_no_query(self):
    #     # Test retrieving all temperatures
    #     response = requests.get(BASE_URL_TEMPERATURES)
    #     self.assertEqual(response.status_code, 200, "Failed to retrieve temperatures")
    #     print(f"GET /temperatures SUCCESS: {response.json()}")
    #     print("PASSED")

    # def test_get_temperatures_latitude_query(self):
    #     # Test retrieving temperatures by latitude such that we only get the temperatures for the base city
    #     response = requests.get(f"{BASE_URL_TEMPERATURES}?lat=46.7712")
    #     self.assertEqual(response.status_code, 200, "Failed to retrieve temperatures by latitude")
    #     print(f"GET /temperatures?lat=46.7712 SUCCESS: {response.json()}")
    #     # Assert that we only have 2 temperatures for the base city
    #     self.assertEqual(len(response.json()), 2, "Failed to filter temperatures by latitude")
    #     print("PASSED")

    # def test_get_temperatures_longitude_query(self):
    #     # Test retrieving temperatures by longitude such that we only get the temperatures for the secondary city
    #     response = requests.get(f"{BASE_URL_TEMPERATURES}?lon=25.6012")
    #     self.assertEqual(response.status_code, 200, "Failed to retrieve temperatures by longitude")
    #     print(f"GET /temperatures?lon=25.6012 SUCCESS: {response.json()}")
    #     # Assert that we only have 2 temperatures for the secondary city
    #     self.assertEqual(len(response.json()), 2, "Failed to filter temperatures by longitude")
    #     print("PASSED")

    def test_get_temperatures_from_query(self):
        # Test retrieving temperatures from a few years ago in order to receive 4 temperatures
        response = requests.get(f"{BASE_URL_TEMPERATURES}?from=2019-01-01")
        self.assertEqual(response.status_code, 200, "Failed to retrieve temperatures from a specific date")
        print(f"GET /temperatures?from=2019-01-01 SUCCESS: {response.json()}")
        # Assert that we have 4 temperatures
        self.assertEqual(len(response.json()), 4, "Failed to filter temperatures from a specific date")

        # Test retrieving temperatures from a date in the future in order to receive 0 temperatures
        response = requests.get(f"{BASE_URL_TEMPERATURES}?from=2028-01-01")
        self.assertEqual(response.status_code, 200, "Failed to retrieve temperatures from a specific date")
        print(f"GET /temperatures?from=2028-01-01 SUCCESS: {response.json()}")
        # Assert that we have 0 temperatures
        self.assertEqual(len(response.json()), 0, "Failed to filter temperatures from a specific date")

        print("PASSED")

    def test_get_temperatures_until_query(self):
        # Test retrieving temperatures until a specific date in the past in order to receive 0 temperatures
        response = requests.get(f"{BASE_URL_TEMPERATURES}?until=2019-01-01")
        self.assertEqual(response.status_code, 200, "Failed to retrieve temperatures until a specific date")
        print(f"GET /temperatures?until=2019-01-01 SUCCESS: {response.json()}")
        # Assert that we have 0 temperatures
        self.assertEqual(len(response.json()), 0, "Failed to filter temperatures until a specific date")

        # Test retrieving temperatures until a date in the future in order to receive 4 temperatures
        response = requests.get(f"{BASE_URL_TEMPERATURES}?until=2028-01-01")
        self.assertEqual(response.status_code, 200, "Failed to retrieve temperatures until a specific date")
        print(f"GET /temperatures?until=2028-01-01 SUCCESS: {response.json()}")
        # Assert that we have 4 temperatures
        self.assertEqual(len(response.json()), 4, "Failed to filter temperatures until a specific date")

        print("PASSED")

    def test_get_temperatures_all_queries(self):
        # Test retrieving temperatures by latitude, longitude, and date
        response = requests.get(f"{BASE_URL_TEMPERATURES}?lat=46.7712&lon=23.6236&from=2019-01-01&until=2028-01-01")
        self.assertEqual(response.status_code, 200, "Failed to retrieve temperatures by latitude, longitude, and date")
        print(f"GET /temperatures?lat=46.7712&lon=23.6236&from=2019-01-01&until=2028-01-01 SUCCESS: {response.json()}")
        # Assert that we have 2 temperatures
        self.assertEqual(len(response.json()), 2, "Failed to filter temperatures by latitude, longitude, and date")

        print("PASSED")


#     def test_post_temperature_invalid_city(self):
#         """Test adding a temperature with an invalid city ID (Fail Case)"""
#         payload = {"id_oras": "000000000000000000000000", "valoare": 30.0}
#         response = requests.post(BASE_URL_TEMPERATURES, json=payload)
#         self.assertEqual(response.status_code, 404, "Invalid city ID not handled")
#         print(f"POST /temperatures FAIL (Invalid City): {response.json()}")

#     def test_get_country_temperatures(self):
#         """Test retrieving temperatures for a specific country"""
#         # Add a temperature
#         temp_payload = {"id_oras": self.city_id, "valoare": 22.5}
#         temp_response = requests.post(BASE_URL_TEMPERATURES, json=temp_payload)
#         self.assertEqual(temp_response.status_code, 201, f"Failed to add temperature: {temp_response.json()}")

#         # Retrieve temperatures by country
#         response = requests.get(f"{BASE_URL_TEMPERATURES}/countries/{self.country_id}")
#         self.assertEqual(response.status_code, 200, "Failed to retrieve country temperatures")
#         print(f"GET /temperatures/countries/{self.country_id} SUCCESS: {response.json()}")

#     def test_put_temperature_success(self):
#         """Test updating a temperature (Success Case)"""
#         # Add a temperature
#         temp_payload = {"id_oras": self.city_id, "valoare": 20.0}
#         temp_response = requests.post(BASE_URL_TEMPERATURES, json=temp_payload)
#         self.assertEqual(temp_response.status_code, 201, f"Failed to add temperature: {temp_response.json()}")
#         temp_id = temp_response.json()["id"]

#         # Update the temperature
#         update_payload = {"id_oras": self.city_id, "valoare": 25.0}
#         response = requests.put(f"{BASE_URL_TEMPERATURES}/{temp_id}", json=update_payload)
#         self.assertEqual(response.status_code, 200, "Failed to update temperature")
#         print(f"PUT /temperatures/{temp_id} SUCCESS: {response.json()}")

#     def test_put_temperature_not_found(self):
#         """Test updating a non-existent temperature (Fail Case)"""
#         payload = {"id_oras": "000000000000000000000000", "valoare": 25.0}
#         response = requests.put(f"{BASE_URL_TEMPERATURES}/000000000000000000000000", json=payload)

#         self.assertEqual(response.status_code, 404, "Non-existent temperature not handled")
#         try:
#             print(f"PUT /temperatures/000000000000000000000000 FAIL: {response.json()}")
#         except requests.exceptions.JSONDecodeError:
#             print(f"PUT /temperatures/000000000000000000000000 FAIL: {response.text}")

if __name__ == "__main__":
    unittest.main()
