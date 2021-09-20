#!/usr/bin/python3
""" Creates blueprint app_views """
from flask import Blueprint
from flask_cors import CORS

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
CORS(app_views, resources={r"/api/*":{"origins":"0.0.0.0"}})

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
