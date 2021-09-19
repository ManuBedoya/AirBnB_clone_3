#!/usr/bin/python3
""" This module creates view for City objects """
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def display_places(city_id):
    """display the cities of a place"""
    try:
        cities = storage.get(City, city_id)
        if cities is None:
            abort(404)
        places_list = []
        all_places = storage.all(Place)
        for place in all_places.values():
            if place.city_id == city_id:
                places_list.append(place.to_dict())
        return jsonify(places_list)
    except:
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False)
def display_place(place_id):
    """display a place"""
    try:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        return jsonify(place.to_dict())
    except:
        abort(404)


@app_views.route(
    'places/<place_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_place(place_id):
    """ Deletes a place """
    try:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    except:
        abort(404)


@app_views.route(
    '/cities/<city_id>/places',
    methods=['POST'],
    strict_slashes=False)
def post_place(city_id):
    """ Create new place """
    try:
        if storage.get(City, city_id) is None:
            abort(404)
        if not request.get_json():
            return jsonify({'error': 'Not a JSON'}), 400
        if 'user_id' not in list(request.get_json().keys()):
            return jsonify({'error': 'Missing user_id'}), 400
        if 'name' not in list(request.get_json().keys()):
            return jsonify({'error': 'Missing name'}), 400
        request_place = request.get_json().copy()
        request_place['city_id'] = city_id
        place = Place(**request_place)
        place.save()
        return jsonify(place.to_dict()), 201
    except:
        abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """ update place with specified id """
    try:
        place = storage.get(City, place_id)
        if place is None:
            abort(404)
        if not request.get_json():
            return jsonify({'error': 'Not a JSON'}), 400
        att_check = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in request.get_json().items():
            if key not in att_check:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
    except:
        abort(404)
