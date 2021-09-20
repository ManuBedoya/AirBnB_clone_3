#!/usr/bin/python3
""" This module creates view for City objects """
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.amenity import Amenity


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
@app_views.route('/amenities', strict_slashes=False)
def display_amenities(amenity_id=None):
    """display all amenities or specified"""
    if amenity_id is None:
        amenity = []
        for value in storage.all(Amenity).values():
            amenity.append(value.to_dict())
    else:
        try:
            amenity = storage.get(Amenity, amenity_id).to_dict()
        except:
            abort(404)

    return jsonify(amenity)


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes an amenity """
    try:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    except:
        abort(404)


@app_views.route(
    '/amenities',
    methods=['POST'],
    strict_slashes=False)
def post_amenity():
    """ Create an amenity """
    try:
        if not request.get_json():
            return jsonify({'error': 'Not a JSON'}), 400
        if 'name' not in list(request.get_json().keys()):
            return jsonify({'error': 'Missing name'}), 400
        amenity = Amenity(**request.get_json())
        amenity.save()
        return jsonify(amenity.to_dict()), 201
    except:
        abort(404)


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['PUT'],
    strict_slashes=False)
def put_amenity(amenity_id):
    """ update amenity with specified id """
    try:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        if not request.get_json():
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    except:
        abort(404)
