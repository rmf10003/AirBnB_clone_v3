#!/usr/bin/python3
"""Module to handle place restful API actions"""

import models
from flask import Flask, jsonify, request, abort, make_response
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['GET'])
def place_all(city_id):
    """Retrives a list of all place objects"""
    cities = models.storage.all('City')
    city_key = 'City.' + city_id
    place_list = []
    if city_key in cities.keys():
        city = cities.get(city_key)
    else:
        abort(404)
    for place in city.places:
        place_list.append(place.to_dict())
    return(jsonify(place_list))


@app_views.route('/places/<place_id>', methods=['GET'])
def place_grab(place_id):
    """grab one place based on ID"""
    places = models.storage.all('Place')
    for key in places.keys():
        c, p, id = key.partition('.')
        if id == place_id:
            return (jsonify(places.get(key).to_dict()))
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def place_del(place_id):
    """delete a place object"""
    places = models.storage.all('Place')
    for key in places.keys():
        s, p, id = key.partition('.')
        if id == place_id:
            models.storage.delete(places.get(key))
            models.storage.save()
            return (jsonify({}))
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['POST'])
def place_create(city_id):
    """Creates a place Object"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, "Missing user_id")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    cities = models.storage.all('City')
    city_key = 'City.' + city_id
    place_list = []
    if city_key not in cities.keys():
        abort(404)
    name = request.get_json()
    place = models.place.Place(city_id=city_id, **name)
    users = models.storage.all('User')
    for user in users.values():
        if place.user_id == user.id:
            models.storage.new(place)
            models.storage.save()
            return make_response(jsonify(place.to_dict()), 201)
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'])
def place_change(place_id):
    """update a place object"""
    if not request.get_json():
        abort(400, "Not a JSON")
    places = models.storage.all('Place')
    for key in places.keys():
        s, p, id = key.partition('.')
        if id == place_id:
            for k, v in request.get_json().items():
                if k not in (
                        'id', 'user_id',
                        'city_id', 'created_at',
                        'updated_at'
                ):
                    setattr(places[key], k, v)
            models.storage.save()
            return (jsonify(places[key].to_dict()))
    abort(404)
