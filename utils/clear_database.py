from pymongo import MongoClient

def clear_database():
    # MongoDB connection
    client = MongoClient("mongodb://localhost:27017/")
    db = client["weather_db"]
    collections = db.list_collection_names()

    # Collection clearing
    for collection in collections:
        result = db[collection].delete_many({})
        print(f"Cleared {result.deleted_count} entries from collection '{collection}'.")

    print("Database cleared successfully!")

if __name__ == "__main__":
    clear_database()
