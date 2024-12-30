#!/usr/bin/python3
"""
Creating a new view forn state that handles all default RESTFul API actions
"""
from flask import Flask, jsonify, abort
from models import storage
from api.v1.views import app_views
from models.state import State

@app_views.route('/api/v1/states', methods=["GET"])
def state_list():
    """retrieves a list of all states"""
    states = storage.all(State).values()
    new_list = [state.to_dict() for state in states]
    return jsonify(new_list)

@app_views.route('/api/v1/states/<state_id>', methods=["GET"])
def state_with_id(state_id):
    """retrives states with its id"""
    state = State.query.get(state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)

@app_views.route('/api/v1/states/<state_id>', methods=["DELETE"])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        return jsonify({}), 200
    else:
        abort(404)

@app_views.route('/api/v1/states', methods=["POST"])
def create_state():
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in list(data.keys()):
        abort(400, 'Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201

@app_views.route('/api/v1/states/<state_id>', methods=["PUT"])
def update_state(state_id):
    state = State.query.get(state_id)
    if state:
        if not request.get.json():
            abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'update_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)


