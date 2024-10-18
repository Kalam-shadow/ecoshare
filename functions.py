from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['eternal']  # Replace with your database name

# Function to register a new user
@app.route('/register', methods=['POST'])
def register_user():
    user_data = request.json
    username = user_data.get('username')
    email = user_data.get('email')
    password = user_data.get('password')

    if db.users.find_one({"username": username}):
        return jsonify({"error": "Username already exists"}), 400

    new_user = {
        "username": username,
        "email": email,
        "password": password  # Remember to hash passwords in production!
    }
    result = db.users.insert_one(new_user)
    return jsonify({"msg": "User registered", "user_id": str(result.inserted_id)}), 201

# Function to check if a user exists
@app.route('/check_user', methods=['POST'])
def check_user():
    user_data = request.json
    username = user_data.get('username')

    user = db.users.find_one({"username": username})
    if user:
        return jsonify({"exists": True, "user_id": str(user['_id'])}), 200
    else:
        return jsonify({"exists": False}), 404

# Function to buy an item
@app.route('/buy', methods=['POST'])
def buy_item():
    purchase_data = request.json
    buyer_username = purchase_data.get('buyer_username')
    item_id = purchase_data.get('item_id')

    item = db.items.find_one({"_id": ObjectId(item_id)})
    if not item:
        return jsonify({"error": "Item not found"}), 404

    transaction = {
        "buyer": buyer_username,
        "item_id": item_id,
        "item_name": item.get('name'),
        "price": item.get('price'),
    }
    db.transactions.insert_one(transaction)
    return jsonify({"msg": "Purchase successful", "transaction_id": str(transaction['_id'])}), 201

# Function to sell an item
@app.route('/sell', methods=['POST'])
def sell_item():
    sell_data = request.json
    seller_username = sell_data.get('seller_username')
    item_name = sell_data.get('item_name')
    price = sell_data.get('price')

    new_item = {
        "seller": seller_username,
        "name": item_name,
        "price": price
    }
    result = db.items.insert_one(new_item)
    return jsonify({"msg": "Item listed for sale", "item_id": str(result.inserted_id)}), 201

# Function to donate an item
@app.route('/donate', methods=['POST'])
def donate_item():
    donate_data = request.json
    donor_username = donate_data.get('donor_username')
    item_name = donate_data.get('item_name')

    new_donation = {
        "donor": donor_username,
        "name": item_name
    }
    result = db.donations.insert_one(new_donation)
    return jsonify({"msg": "Donation successful", "donation_id": str(result.inserted_id)}), 201

if __name__ == '__main__':
    app.run(debug=True)
