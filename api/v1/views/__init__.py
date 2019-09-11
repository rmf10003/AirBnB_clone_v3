#!usr/bin/python3
"""Init file that sets up our module"""

from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
import api.v1.views.states
import apo.v1.views.cities
import apo.v1.views.amenities
# import apo.v1.views.users
# import apo.v1.views.places
# import apo.v1.views.places_reviews
