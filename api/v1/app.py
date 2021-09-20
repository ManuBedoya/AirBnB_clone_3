#!/usr/bin/python3
""" Creates app with Flask instance """
from flask import Flask, jsonify, abort
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    """ Tears down the session """
    storage.close()


@app.errorhandler(404)
def invalid_route(e):
    """ Redirects to 404 json message if error occurs """
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
