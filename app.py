# app.py
# Task 4: Build a REST API with Flask

from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data storage for users
# Each user has an id, name, and email
users = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"}
}

# Helper function to generate the next user ID
def get_next_id():
    if users:
        return max(users.keys()) + 1
    return 1


# ---------------------- GET: Retrieve All Users ----------------------
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200


# ---------------------- GET: Retrieve Single User ----------------------
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if user_id in users:
        return jsonify({user_id: users[user_id]}), 200
    return jsonify({"error": "User not found"}), 404


# ---------------------- POST: Add a New User ----------------------
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()

    # Validate input
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name and email are required"}), 400

    user_id = get_next_id()
    users[user_id] = {
        "name": data['name'],
        "email": data['email']
    }

    return jsonify({
        "message": "User added successfully",
        "user_id": user_id,
        "user": users[user_id]
    }), 201


# ---------------------- PUT: Update an Existing User ----------------------
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Update fields if provided
    users[user_id]['name'] = data.get('name', users[user_id]['name'])
    users[user_id]['email'] = data.get('email', users[user_id]['email'])

    return jsonify({
        "message": "User updated successfully",
        "user": users[user_id]
    }), 200


# ---------------------- DELETE: Remove a User ----------------------
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    deleted_user = users.pop(user_id)

    return jsonify({
        "message": "User deleted successfully",
        "user": deleted_user
    }), 200


# ---------------------- Root Endpoint ----------------------
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Welcome to the User Management REST API",
        "endpoints": {
            "GET /users": "Retrieve all users",
            "GET /users/<id>": "Retrieve a specific user",
            "POST /users": "Add a new user",
            "PUT /users/<id>": "Update an existing user",
            "DELETE /users/<id>": "Delete a user"
        }
    })


# ---------------------- Run the Flask Application ----------------------
if __name__ == '__main__':
    app.run(debug=True)