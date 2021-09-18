#!/usr/bin/python3
""" Routes related to app_views blueprint """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def show_status():
    """ Shows status of an endpoint. """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def gives_stats():
    """ Counts the amount of objects of each class. """
    from models.engine.db_storage import classes
    from models import storage
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    dict_count = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(dict_count)
