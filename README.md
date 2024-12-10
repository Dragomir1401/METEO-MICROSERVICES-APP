# Weather Data REST API Microservices Project

#### Dragomir Andrei-Mihai 343C1

This project implements a weather data management system using a **Python Flask REST API** connected to a **MongoDB database**, containerized with **Docker**. The solution handles geographical data (countries, cities, temperatures) and provides a suite of API routes for managing these entities.

## How to Build & Run

This project uses **Docker Compose** to manage and orchestrate the containers for the REST API, MongoDB database, and a MongoDB management utility (Mongo Express). Below are detailed steps on how to build and run the application.

### Docker Compose Overview

The `docker-compose.yml` file is configured as follows:

- **Services**:

  - **api**: Flask REST API service that connects to MongoDB.
  - **db**: MongoDB database for storing application data.
  - **mongo-express**: Web interface to manage MongoDB.

- **Networks**:

  - `api_network`: Connects the Flask API and MongoDB.
  - `db_util_network`: Connects Mongo Express to MongoDB for database management.

- **Volumes**:
  - `mongo_data`: Persistent volume to store MongoDB data.

### Prerequisites

- Install [Docker](https://www.docker.com/).
- Install [Docker Compose](https://docs.docker.com/compose/).
- Clone the project repository to your local machine.

### Run

- Start docker daemon or docker desktop
- Run `docker-compose up`

---

## Features

- **REST API**: Endpoints for managing countries, cities, and temperatures, consuming and returning JSON objects.
- **Database Integration**: MongoDB as the backend database with a predefined schema.
- **Dockerized Solution**: Configurable Docker Compose setup for easy deployment.
- **Self-Made Test Suite**: Comprehensive tests to verify API functionality.

---

## API Endpoints

### Countries

- **POST** `/api/countries`: Add a country.
  **Body**: `{ "nume": "Str", "lat": "Double", "lon": "Double" }`
- **GET** `/api/countries`: Retrieve all countries.
- **PUT** `/api/countries/:id`: Update a country's details.
  **Body**: `{ "id": "Int", "nume": "Str", "lat": "Double", "lon": "Double" }`
- **DELETE** `/api/countries/:id`: Delete a country.

### Cities

- **POST** `/api/cities`: Add a city.
  **Body**: `{ "idTara": "Int", "nume": "Str", "lat": "Double", "lon": "Double" }`
- **GET** `/api/cities`: Retrieve all cities.
- **GET** `/api/cities/country/:id_Tara`: Retrieve cities by country.
- **PUT** `/api/cities/:id`: Update a city.
  **Body**: `{ "id": "Int", "idTara": "Int", "nume": "Str", "lat": "Double", "lon": "Double" }`
- **DELETE** `/api/cities/:id`: Delete a city.

### Temperatures

- **POST** `/api/temperatures`: Add a temperature record.
  **Body**: `{ "id_oras": "Int", "valoare": "Double" }`
- **GET** `/api/temperatures`: Retrieve temperatures based on filters (latitude, longitude, date range).
- **GET** `/api/temperatures/cities/:id_oras`: Retrieve temperatures for a city.
- **GET** `/api/temperatures/countries/:id_tara`: Retrieve temperatures for a country.
- **PUT** `/api/temperatures/:id`: Update a temperature record.
  **Body**: `{ "id": "Int", "idOras": "Int", "valoare": "Double" }`
- **DELETE** `/api/temperatures/:id`: Delete a temperature record.

---

## Database Schema

- **Countries**

  ```json
  {
    "id": "ObjectId",
    "nume": "String",
    "lat": "Double",
    "lon": "Double"
  }
  ```

- **Cities**

  ```json
  {
    "id": "ObjectId",
    "idTara": "ObjectId",
    "nume": "String",
    "lat": "Double",
    "lon": "Double"
  }
  ```

- **Temperatures**

  ```json
  {
    "id": "ObjectId",
    "idOras": "ObjectId",
    "valoare": "Double",
    "timestamp": "Date"
  }
  ```

## Test options

- **Utils**
  --**utils/clear_database.py** - removes all entries from database
  --**utils/drop_indexes.py** - drops the tables in the database

- **JSON tests** - tests/colletion/tests.json - can be imported in Postman or other similar application

  > ⚠️ **Important:** Before running the collection make sure you run utils/clear_database.py to clear all entries first.

- **Automated py tests**
  --**_tests/test_countries.py_**
  --**_test/test_cities.py_**
  --**_test/test_temperatures.py_**
  This py tests have built in clearing of database in the tests init.

```

```
