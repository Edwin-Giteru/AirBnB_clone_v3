#!/usr/bin/python3
"""
a view for for City objects that handles all default RESTFul API
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City

@app_views.route('/api/v1/states/<state_id>/cities', methods=["GET"])
def state_cities_list(state_id):
    """retrieves the state id"""
    state = storage.query.get(state_id)
    if state:
        cities = state.cities()
        cities_list = [City.to_dict() for City in cities]
        return jsonify(cities_list)
    else:
        abort(404)

@app_views.route('/api/v1/cities/<city_id>', methods=["GET"])
def cities_with_id(city_id):
    """retrieves city's id"""
    city = City.query.get(city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)

@app_views.route('/api/v1/cities/<city_id>')
def delete_city(city_id):
    city = City.query.get(city_id)
    if city:
        storage.delete(city)
        return jsonify({}), 200
    else:
        abort(404)

@app_views.route('/api/v1/states/<state_id>/cities', methods=["POST"])
def create_city():
    data = request.get_json()
    if not data:
        abort(400), 'Not a JSON'
    if 'name' not in list(data.keys()):
        abort(400), 'Missing Name'

    new_city = State(**data)
    new_city.save()
    return jsonify(new_city)

@app_views.route('/api/v1/cities/<city_id>', methods=["PUT"])
def update_city(city_id):
    city = City.query.get(city_id)
    if city:
        if not request.get_json():
            abort(400), 'Not a JSON'
        data = request.get_json()
        ignore_keys = [id, state_id, created_at, updated_at]
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)
        city.save()
        return  jsonify(city.to_dict()), 200
    else:
        abort(404)

