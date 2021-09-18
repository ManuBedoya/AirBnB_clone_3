#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
""" Routes related to app_views blueprint """

@app_views.route('/status')
def show_status():
    """ Shows status of an endpoint. """
    return jsonify({"status": "OK"})
