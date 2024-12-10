from pymongo import MongoClient, ASCENDING

# MongoDB Connection
client = MongoClient("mongodb://db:27017/")
db = client["weather_db"]

# Country Collection
tari = db["tari"]
tari.create_index([("nume", ASCENDING)], unique=True)

# City Collection
orase = db["orase"]
orase.create_index([("nume", ASCENDING), ("id_tara", ASCENDING)], unique=True)

# Temperature Collection
temperaturi = db["temperaturi"]
temperaturi.create_index([("idOras", ASCENDING), ("timestamp", ASCENDING)], unique=True)
