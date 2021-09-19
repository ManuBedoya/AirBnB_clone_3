#!/usr/bin/python3
""" This module creates view for State objects """
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort
from models.state import State


@app_views.route('/states', strict_slashes=False)
@app_views.route('/states/<state_id>', strict_slashes=False)
def display_states(state_id=None):
    """display the states and cities listed in alphabetical order"""
    if state_id is None:
        states = []
        for value in storage.all().values():
            states.append(value.to_dict())
    else:
        try:
            states = storage.get(State, state_id).to_dict()
        except:
            abort(404)

    return jsonify(states)

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_states(state_id):
    """ Deletes a state """
    try:
        state = storage.get(State, state_id)
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    except:
        abort(404)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states(state_id):
    """ Create new state """
    try:
        if not request.get_json():
            return jsonify({'error': 'Not a JSON'}), 400
        if name not in request.get_json():
            return jsonify({'error': 'Missing name'}), 400

        state = State(**request.get_json())
        state.save()
        return jsonify({state}), 201
    except:
        abort(404)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_states(state_id):
    """ update state """
    try:
        state = storage.get(State, state_id)
        if not request.get_json():
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in request.get_json().items():
            if key not in State.__dict__.keys():
                setattr(state, key, value)
        state.save()
        return jsonify({state}), 201
    except:
        abort(404)
