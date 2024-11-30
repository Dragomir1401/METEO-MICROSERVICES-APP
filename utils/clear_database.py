from pymongo import MongoClient

def clear_database():
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")  # Change if running on a different host/port
    db = client["weather_db"]

    # Get all collections in the database
    collections = db.list_collection_names()

    # Clear each collection
    for collection in collections:
        result = db[collection].delete_many({})
        print(f"Cleared {result.deleted_count} entries from collection '{collection}'.")

    print("Database cleared successfully!")

if __name__ == "__main__":
    clear_database()
