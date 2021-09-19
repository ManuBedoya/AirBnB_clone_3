#!/usr/bin/python3
""" This module creates view for Review objects """
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def display_reviews(place_id):
    """display the places review"""
    try:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        review_list = []
        all_reviews = storage.all(Review)
        for review in all_reviews.values():
            if review.place_id == place_id:
                review_list.append(review.to_dict())
        return jsonify(review_list)
    except:
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def display_review(review_id):
    """display a review"""
    try:
        review = storage.get(Review, review_id)
        if review is None:
            abort(404)
        return jsonify(review.to_dict())
    except:
        abort(404)


@app_views.route(
    '/reviews/<review_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_review(review_id):
    """ Deletes a review """
    try:
        review = storage.get(Review, review_id)
        if review is None:
            abort(404)
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    except:
        abort(404)


@app_views.route(
    '/places/<place_id>/reviews',
    methods=['POST'],
    strict_slashes=False)
def post_review(place_id):
    """ Create new review """
    try:
        if storage.get(Place, place_id) is None:
            abort(404)
        if not request.get_json():
            return jsonify({'error': 'Not a JSON'}), 400
        if 'user_id' not in list(request.get_json().keys()):
            return jsonify({'error': 'Missing user_id'}), 400
        if 'text' not in list(request.get_json().keys()):
            return jsonify({'error': 'Missing text'}), 400
        request_review = request.get_json().copy()
        user = storage.get(User, request_review['user_id'])
        if user is None:
            abort(404)
        request_review['place_id'] = place_id
        review = Review(**request_review)
        review.save()
        return jsonify(review.to_dict()), 201
    except:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """ update review with specified id """
    try:
        review = storage.get(Review, review_id)
        if review is None:
            abort(404)
        if not request.get_json():
            return jsonify({'error': 'Not a JSON'}), 400
        check_attr = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in request.get_json().items():
            if key not in check_attr:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
    except:
        abort(404)
