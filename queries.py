from pymongo import MongoClient

# Function to initialize and return MongoDB collection
def get_mongo_client():
    client = MongoClient("mongodb+srv://<username>:<password>@<cluster-url>/resource_sharing_db")
    db = client.resource_sharing_db
    return db

# Fetch listed items for donation
def fetch_listed_items():
    db = get_mongo_client()
    listed_items = list(db.listed_items.find())  # Convert cursor to list
    return listed_items if listed_items else []  # Ensure null safety

# Fetch donated items
def fetch_donated_items():
    db = get_mongo_client()
    donated_items = list(db.donated_items.find())  # Convert cursor to list
    return donated_items if donated_items else []  # Ensure null safety
