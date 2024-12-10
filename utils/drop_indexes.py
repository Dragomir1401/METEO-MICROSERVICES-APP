from pymongo import MongoClient

def drop_all_indexes():
    # MongoDB Connection
    client = MongoClient("mongodb://localhost:27017/")
    db = client["weather_db"]
    collections = db.list_collection_names()

    # Index dropping
    for collection in collections:
        db[collection].drop_indexes()
        print(f"Dropped all indexes from collection '{collection}'.")

if __name__ == "__main__":
    drop_all_indexes()
