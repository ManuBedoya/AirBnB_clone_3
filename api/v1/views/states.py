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

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_states(state_id):
    """ Deletes a state """
    try:
        state = storage.get(State, state_id)
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    except:
        abort(404)
