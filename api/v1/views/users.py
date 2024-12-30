#!/usr/bin/python3
"""
user API
"""
from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.user import User

@app_views.route('/api/v1/users', methods=["GET"])
def list_users():
    users = storage.all(User).values()
    users = [user.to_dict() for user in users]

    return jsonify(users)

@app_views.route('/api/v1/users/<user_id>', methods=["GET"])
def users_with_ids(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user)

@app_views.route('/api/v1/users/<user_id>', methods=["DELETE"])
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    return jsonify({}), 200

@app_views.route('/api/v1/users',methods=["POST"])
def add_user():
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, "Not a JSON")
    if 'email' not in data:
        abort(400, "Missing email")
    if 'password' not in data:
        abort(400, "Missing password")
    user = User()
    for key, val in data.items():
        setattr(user, key, val)
    return jsonify(user.to_dict()), 200

@app_views.route('/api/v1/users/<user_id>', methods=["PUT"])
def update_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict):
        abort(404, "Not a JSON")
    ignore_keys = ["id", "email", "created_at", "updated_at"]
    for key, val data.items():
        if key not in ignore_keys:
            setattr(user, key, val)
    return jsonify(user.to_dict()), 200

