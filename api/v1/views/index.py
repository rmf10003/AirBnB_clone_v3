#!/usr/bin/python3
"""Module to create a route"""

from api.v1.views import app_views
from flask import jsonify
import models


@app_views.route('/status')
def status():
    """Returns a JSON status"""
    return (jsonify(status="OK"))


@app_views.route('/stats')
def num_objects():
    """Retrieves the number of objects by type"""
    classes = {"Amenity": "amenities", "City": "cities", "Place": "places",
               "Review": "reviews", "State": "states", "User": "users"}
    new_dict = {}
    for key, value in classes.items():
        new_dict[value] = models.storage.count(key)
    return (jsonify(new_dict))
