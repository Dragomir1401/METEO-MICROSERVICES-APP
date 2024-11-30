from pymongo import MongoClient, ASCENDING

# MongoDB Connection
client = MongoClient("mongodb://db:27017/")
db = client["weather_db"]

# Tari Collection
tari = db["Tari"]
tari.create_index([("nume_tara", ASCENDING)], unique=True)

# Orase Collection
orase = db["Orase"]
orase.create_index([("id_tara", ASCENDING), ("nume_oras", ASCENDING)], unique=True)

# Temperaturi Collection
temperaturi = db["Temperaturi"]
temperaturi.create_index([("id_oras", ASCENDING), ("timestamp", ASCENDING)], unique=True)
