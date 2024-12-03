from pymongo import MongoClient

def drop_all_indexes():
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")  # Change if running on a different host/port
    db = client["weather_db"]

    # Get all collections in the database
    collections = db.list_collection_names()

    # Drop all indexes from each collection
    for collection in collections:
        db[collection].drop_indexes()
        print(f"Dropped all indexes from collection '{collection}'.")

if __name__ == "__main__":
    drop_all_indexes()
