#!/usr/bin/python3
"""Module to handle review restful API actions"""

import models
from flask import Flask, jsonify, request, abort, make_response
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities',
                 strict_slashes=False,
                 methods=['GET'])
def amenity_place__all(place_id):
    """Retrives a list of all amenity objects"""
    places = models.storage.all('Place')
    place_key = 'Place.' + place_id
    amenity_list = []
    if place_key in places.keys():
        place = places.get(place_key)
    else:
        abort(404)
    for amenity in place.amenities:
        amenity_list.append(amenity.to_dict())
    return(jsonify(amenity_list))


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def amenity_place_del(place_id, amenity_id):
    """delete a amenity object"""
    places = models.storage.all('Place')
    place_key = 'Place.' + place_id
    amenities = models.storage.all('Amenity')
    amenity_key = 'Amenity.' + amenity_id
    if place_key not in places.keys():
        abort(404)
    if amenity_key not in amenities.keys():
        abort(400)
    place = places.get(place_key)
    for amenity in place.amenities:
        if amenity_id == amenity.id:
            models.storage.delete(amenity)
            models.storage.save()
            return (jsonify({}))
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['POST'])
def amenity_link(place_id, amenity_id):
    """Creates a amenity Object"""
    places = models.storage.all('Place')
    place_key = 'Place.' + place_id
    amenities = models.storage.all('Amenity')
    amenity_key = 'Amenity.' + amenity_id
    if place_key not in places.keys():
        abort(404)
    if amenity_key not in amenities.keys():
        abort(400)
    place = places.get(place_key)
    for amenity in place.amenities:
        if amenity_id == amenity.id:
            return jsonify(amenity.to_dict())
    json_dict = jsonify(place.amenities.append(amenities[amenity_key]))
    return make_response(json_dict, 201)
