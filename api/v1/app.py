#!/usr/bin/python3
from flask import Flask
from models import storage
from api.v1.views import app_views
import os
""" Creates app with Flask instance """

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """ Tears down the session """
    storage.close()

if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)