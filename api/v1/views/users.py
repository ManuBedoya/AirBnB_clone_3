#!/usr/bin/python3
""" This module creates view for User objects """
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.user import User


@app_views.route('/users/<user_id>', strict_slashes=False)
@app_views.route('/users', strict_slashes=False)
def display_users(user_id=None):
    """display all users or specified"""
    if user_id is None:
        user = []
        for value in storage.all(User).values():
            user.append(value.to_dict())
    else:
        try:
            user = storage.get(User, user_id).to_dict()
        except:
            abort(404)

    return jsonify(user)


@app_views.route(
    '/users/<user_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_user(user_id):
    """ Deletes a user """
    try:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    except:
        abort(404)


@app_views.route(
    '/users',
    methods=['POST'],
    strict_slashes=False)
def post_users():
    """ Create a user """
    try:
        if not request.get_json():
            return jsonify({'error': 'Not a JSON'}), 400
        if 'email' not in list(request.get_json().keys()):
            return jsonify({'error': 'Missing email'}), 400
        if 'password' not in list(request.get_json().keys()):
            return jsonify({'error': 'Missing password'}), 400
        user = User(**request.get_json())
        user.save()
        return jsonify(user.to_dict()), 201
    except:
        abort(404)


@app_views.route(
    '/users/<user_id>',
    methods=['PUT'],
    strict_slashes=False)
def put_user(user_id):
    """ update user with specified id """
    try:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        if not request.get_json():
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in request.get_json().items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    except:
        abort(404)
