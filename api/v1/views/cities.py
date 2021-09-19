#!/usr/bin/python3
""" This module creates view for State objects """
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models import city
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def display_cities(state_id):
    """display the cities of a state"""
    try:
        states = storage.get(State, state_id)
        if states is None:
            abort(404)
        city_list = []
        all_cities = storage.all(City)
        for city in all_cities.values():
            if city.state_id == state_id:
                city_list.append(city.to_dict())
        return jsonify(city_list)
    except:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def display_city(city_id):
    """display a city"""
    try:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        return jsonify(city.to_dict())
    except:
        abort(404)


@app_views.route(
    '/cities/<city_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_city(city_id):
    """ Deletes a city """
    try:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    except:
        abort(404)


@app_views.route(
    '/states/<state_id>/cities',
    methods=['POST'],
    strict_slashes=False)
def post_city(state_id):
    """ Create new city """
    try:
        if storage.get(State, state_id) is None:
            abort(404)
        if not request.get_json():
            return jsonify({'error': 'Not a JSON'}), 400
        if 'name' not in list(request.get_json().keys()):
            return jsonify({'error': 'Missing name'}), 400
        request_city = request.get_json().copy()
        request_city['state_id'] = state_id
        city = City(**request_city)
        city.save()
        return jsonify(city.to_dict()), 201
    except:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """ update city with specified id """
    try:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        if not request.get_json():
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in request.get_json().items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    except:
        abort(404)
