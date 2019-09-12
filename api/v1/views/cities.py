#!/usr/bin/python3
"""Module to handle city restful API actions"""

import models
from flask import Flask, jsonify, request, abort, make_response
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False,
                 methods=['GET'])
def city_all(state_id):
    """Retrives a list of all city objects"""
    states = models.storage.all('State')
    state_key = 'State.' + state_id
    city_list = []
    if state_key in states.keys():
        state = states.get(state_key)
    else:
        abort(404)
    for city in state.cities:
        city_list.append(city.to_dict())
    return(jsonify(city_list))


@app_views.route('/cities/<city_id>', methods=['GET'])
def city_grab(city_id):
    """grab one city based on ID"""
    cities = models.storage.all('City')
    for key in cities.keys():
        c, p, id = key.partition('.')
        if id == city_id:
            return (jsonify(cities.get(key).to_dict()))
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def city_del(city_id):
    """delete a city object"""
    cities = models.storage.all('City')
    for key in cities.keys():
        s, p, id = key.partition('.')
        if id == city_id:
            models.storage.delete(cities.get(key))
            models.storage.save()
            return (jsonify({}))
    abort(404)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False,
                 methods=['POST'])
def city_create(state_id):
    """Creates a city Object"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    states = models.storage.all('State')
    state_key = 'State.' + state_id
    city_list = []
    if state_key not in states.keys():
        abort(404)
    name = request.get_json()
    city = models.city.City(state_id=state_id, **name)
    models.storage.new(city)
    models.storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def city_change(city_id):
    """update a city object"""
    if not request.get_json():
        abort(400, "Not a JSON")
    cities = models.storage.all('City')
    for key in cities.keys():
        s, p, id = key.partition('.')
        if id == city_id:
            for k, v in request.get_json().items():
                if k not in ('id', 'state_id', 'created_at', 'updated_at'):
                    setattr(cities[key], k, v)
            models.storage.save()
            return (jsonify(cities[key].to_dict()))
    abort(404)
