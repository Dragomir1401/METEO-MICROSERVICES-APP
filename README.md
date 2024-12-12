# Weather Data REST API Microservices Project

#### Dragomir Andrei-Mihai 343C1

This project implements a weather data management system using a **Python Flask REST API** connected to a **MongoDB database**, containerized with **Docker**. The solution handles geographical data (countries, cities, temperatures) and provides a suite of API routes for managing these entities.

#### ⚠️ **Important:** Before running docker-compose up make sure you dont have existing containers with names: flask_api, mongo_db, mongo_express

- **`If so, remove them first`**
  **`docker rm -f flask_api`**
  **`docker rm -f mongo_db`**
  **`docker rm -f mongo_express`**

#### ⚠️ **Important:** Before running the Postman test collection make sure you run python3 utils/clear_database.py to clear all entries first if database does not start as fresh.

## How to Build & Run

This project uses **Docker Compose** to manage and orchestrate the containers for the REST API, MongoDB database, and a MongoDB management utility (Mongo Express). Below are detailed steps on how to build and run the application.

### Docker Compose Overview

The `docker-compose.yml` file is designed to follow best practices for containerized application development, including logical network separation, environment variable usage, and persistent storage. Here's a detailed breakdown of the setup:

#### **Services**

- **`api`**:

  - A Flask-based REST API that provides endpoints for managing countries, cities, and temperatures.
  - Connects to MongoDB (`db`) via the shared `shared_network`.
  - Exposed on port `5001` (configurable via the `API_PORT` environment variable).

- **`db`**:

  - MongoDB instance for storing the apps data, such as countries, cities, and temperatures.
  - Accessible from both the Flask API (`api`) and Mongo Express (`mongo-express`) through the `shared_network` and `db_network`.
  - Uses a persistent volume `mongo_data` to retain data across container restarts.

- **`mongo-express`**:
  - A web-based UI to interact with the MongoDB database.
  - Runs on port `8081` (configurable via the `MONGO_EXPRESS_PORT` environment variable).
  - Connects to MongoDB (`db`) via the `db_network`.

---

#### **Networks**

To ensure clear separation of concerns and enhance security, the application uses multiple Docker networks:

- **`api_network`**:

  - Dedicated network for the API service to communicate with other internal services.
  - Provides logical isolation for the API from other utility services like `mongo-express`.

- **`db_network`**:

  - Dedicated network for the database (`db`) and `mongo-express`.
  - Isolates the database management tool (`mongo-express`) from the API.

- **`shared_network`**:
  - A shared network that enables the API (`api`) to communicate with the database (`db`) while keeping the `mongo-express` service isolated.

By using these networks, each service only has access to the resources it needs, minimizing potential security risks.

---

#### **Environment Variables**

To enhance flexibility and ease of deployment across different environments (e.g., development, staging, production), the following environment variables are used:

- **`API_PORT`**: Configures the exposed port for the Flask API (default: `5001`).
- **`DB_PORT`**: Configures the exposed port for MongoDB (default: `27017`).
- **`MONGO_EXPRESS_PORT`**: Configures the exposed port for Mongo Express (default: `8081`).
- **`APP_ENV`**: Specifies the environment mode for the API (e.g., `development`, `production`). Default is `development`.

These variables can be set in a `.env` file or passed directly as environment variables when running Docker Compose.

---

#### **Volumes**

Persistent volumes are used to retain critical application data:

- **`mongo_data`**:
  - Stores MongoDB data, ensuring that it is not lost when the container restarts or is recreated.
  - Mapped to the `/data/db` directory in the MongoDB container.

---

#### **Best Practices Implemented**

1. **Logical Network Separation**:

   - Services are grouped into networks based on their interaction requirements, ensuring minimal exposure.
   - The `api` and `db` services communicate through the `shared_network`, while `mongo-express` is isolated in `db_network`.

2. **DNS-Based Service Discovery**:

   - Containers refer to each other by their service names (e.g., `db`) instead of hardcoded IP addresses, enabling seamless integration and portability.

3. **Environment Variables**:

   - Port configurations and other settings are externalized for easy customization and flexibility across different environments.

4. **Data Persistence**:
   - MongoDB data is stored in a persistent Docker volume (`mongo_data`) to prevent data loss during container restarts.

---

## **How to Run**

1. Create a `.env` file in the project root with the following content (example values):
   ```env
   API_PORT=5001
   DB_PORT=27017
   MONGO_EXPRESS_PORT=8081
   APP_ENV=development
   ```
   Or use the one provided in the repo.

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
  **Note**: Id can also be provided in the body and in the path. The one in the path will be prioritised so a good id in the path and a bad one in body will yield a good result.
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
  _python3_ **utils/clear_database.py** - removes all entries from database
  _python3_ **utils/drop_indexes.py** - drops the tables in the database

- **JSON tests** - tests/colletion/tests.json - can be imported in Postman or other similar application

  > ⚠️ **Important:** Before running the collection make sure you run utils/clear_database.py to clear all entries first.

- **Automated py tests**
  --**_tests/test_countries.py_**
  --**_test/test_cities.py_**
  --**_test/test_temperatures.py_**
  This py tests have built in clearing of database in the tests init.

```

```
