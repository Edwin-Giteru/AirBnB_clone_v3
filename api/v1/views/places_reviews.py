#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from flask import jsonify, abort, request

@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_by_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = storage.all(Review).values()
    reviews_list = [review.to_dict() for review in reviews if review.place_id == place_id]
    return jsonify(reviews_list)

@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    details = request.get_json()
    if not isinstance(details, dict):
        abort(400, "Not a JSON")
    if "user_id" not in details.keys():
        abort(400, "Missing user_id")
    if "text" not in details.keys():
        abort(400, "Missing text")
    review = Review()
    for key, val in details.items():
        setattr(review, key, val)
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    details = request.get_json()
    if not isinstance(details, dict):
        abort(400, "Not a JSON")
    to_be_ignored = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, val in details.items():
        if key not in to_be_ignored:
            setattr(review, key, val)
    return jsonify(review.to_dict()), 200
