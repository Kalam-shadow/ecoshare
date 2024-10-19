from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import re
from urllib.parse import quote_plus  # Import for URL encoding
import datetime

app = Flask(__name__)

username = quote_plus('adithyas26')
password = quote_plus('admin123')

# Update the MongoDB connection string with the encoded credentials
client = MongoClient(f'mongodb+srv://{username}:{password}@cluster0.t6keu.mongodb.net/')
db = client['Eternal']  # Replace with your database name

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_data = request.json  # Get JSON data
        username = user_data.get('username')
        password = user_data.get('password')

        # Fetch user from MongoDB
        user = db.users.find_one({"username": username})

        # Check if user exists and verify the password (no hashing for now)
        if user and password == user['password']:
            return jsonify({"msg": "Login successful"}), 200  # Respond with success
        else:
            return jsonify({"error": "Invalid username or password"}), 401  # Respond with error

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_data = request.json  # Get JSON data from the request
        name = user_data.get('name')
        username = user_data.get('username')
        email = user_data.get('email')
        password = user_data.get('password')

        # Basic validation
        if db.users.find_one({"username": username}):
            return jsonify({"error": "Username already exists"}), 400

        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):  # Validate email format
            return jsonify({"error": "Invalid email address"}), 400

        if len(password) < 8:  # Ensure password length is at least 8 characters
            return jsonify({"error": "Password must be at least 8 characters long"}), 400

        new_user = {
            "username": username,
            "email": email,
            "password": password  # Storing plain password (will add encryption later)
        }
        
        db.users.insert_one(new_user)  # Save user to MongoDB
        return jsonify({"msg": "User registered successfully"}), 201

    return render_template('signup.html')  # Render the signup form for GET requests

@app.route('/postitem', methods=['GET', 'POST'])
def post_item():
    if request.method == 'POST':
        # Get the form data
        item_data = request.form  # If using a form in HTML
        item_name = item_data.get('item_name')
        item_description = item_data.get('item_description')
        item_category = item_data.get('item_category')  # Example category field
        item_owner = item_data.get('item_owner')  # Example of user submitting the item

        # Basic validation
        if not item_name or not item_description or not item_owner:
            return jsonify({"error": "All fields are required"}), 400

        # Create the item document to insert into MongoDB
        new_item = {
            "item_name": item_name,
            "item_description": item_description,
            "item_category": item_category,
            "item_owner": item_owner,  # Assuming you have a way to track the user
            "created_at": datetime.utcnow()  # Store the current time as the submission time
        }

        # Insert the item into the MongoDB collection (assuming you have an 'items' collection)
        db.items.insert_one(new_item)

        # Redirect to the item submission confirmation page
        return redirect(url_for('submitpage'))

    # If it's a GET request, show the form
    return render_template('postitem.html')

@app.route('/submitpage')
def item_submitted():
    return render_template('submitpage')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        # Implement profile update logic here
        return redirect(url_for('profile'))  # Redirect to profile page after update
    return render_template('profile.html')

@app.route('/view_items')
def view_items():
    # Implement logic to fetch and display user items
    return render_template('view_items.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # This would be your dashboard page

if __name__ == '__main__':
    app.run(debug=True)
