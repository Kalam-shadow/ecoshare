from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from pymongo import MongoClient
from queries import fetch_listed_items, fetch_donated_items
from urllib.parse import quote_plus  # Import for URL encoding
from werkzeug.security import generate_password_hash, check_password_hash  # For hashing passwords
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Add a secret key for session management

# MongoDB connection
username = quote_plus('adithyas26')
password = quote_plus('admin123')
client = MongoClient(f'mongodb+srv://{username}:{password}@cluster0.t6keu.mongodb.net/')
db = client['Eternal']  # Replace with your actual database name

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            user_data = request.get_json()  # Get JSON data
            username = user_data.get('username')
            password = user_data.get('password')
        else:
            # Handle form data (application/x-www-form-urlencoded)
            username = request.form.get('username')
            password = request.form.get('password')

        # Fetch user from MongoDB
        user = db.users.find_one({"username": username})

        # Check if user exists and verify the password (no hashing for now)
        if user and password == user['password']:
            return redirect(url_for('dashboard'))
    # Respond with success
        
        else:
            return jsonify({"error": "Invalid username or password"}), 401  # Respond with error

    return render_template('login.html')




# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validation
        if db.users.find_one({"username": username}):
            return jsonify({"error": "Username already exists"}), 400

        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):  # Email validation
            return jsonify({"error": "Invalid email address"}), 400

        if len(password) < 8:  # Password length check
            return jsonify({"error": "Password must be at least 8 characters long"}), 400

        hashed_password = generate_password_hash(password)  # Hashing the password

        new_user = {
            "username": username,
            "email": email,
            "password": hashed_password  # Storing hashed password
        }

        db.users.insert_one(new_user)  # Save user to MongoDB
        return jsonify({"msg": "User registered successfully"}), 201

    return render_template('signup.html')

# Post Item route
@app.route('/postitem', methods=['GET', 'POST'])
def post_item():
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        item_description = request.form.get('item_description')
        item_category = request.form.get('item_category')
        item_owner = session.get('username')  # Use session to track logged-in user

        # Validation
        if not item_name or not item_description or not item_owner:
            return jsonify({"error": "All fields are required"}), 400

        new_item = {
            "item_name": item_name,
            "item_description": item_description,
            "item_category": item_category,
            "item_owner": item_owner,
            "created_at": datetime.utcnow()  # Store current time
        }

        db.items.insert_one(new_item)  # Insert into MongoDB
        return redirect(url_for('item_submitted'))  # Redirect after submission

    return render_template('postitem.html')

# Item Submitted Page
@app.route('/submitpage')
def item_submitted():
    return render_template('submitpage.html')

# Profile route
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        # Example: updating user profile
        new_email = request.form.get('email')
        new_password = request.form.get('password')
        user_id = session.get('user_id')

        update_fields = {}
        if new_email:
            update_fields['email'] = new_email
        if new_password:
            update_fields['password'] = generate_password_hash(new_password)

        if update_fields:
            db.users.update_one({"_id": user_id}, {"$set": update_fields})

        return redirect(url_for('profile'))

    return render_template('profile.html')

# View Items route
@app.route('/view_items')
def view_items():
    items = list(db.items.find({"item_owner": session.get('username')}))  # Fetch user items
    return render_template('view_items.html', items=items)

# Dashboard route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # User dashboard

# Donation overview route
@app.route('/donation-list')
def donationlist():
    # Fetch the donation items using the functions from the db_queries module
    listed_items = fetch_listed_items()
    donated_items = fetch_donated_items()

    # Render the donation list template with the data
    return render_template('donationlist.html', listed_items=listed_items, donated_items=donated_items)
# Logout route
@app.route('/logout')
def logout():
    session.clear()  # Clear session data on logout
    return redirect(url_for('home'))  # Redirect to home page

if __name__ == '__main__':
    app.run(debug=True)
