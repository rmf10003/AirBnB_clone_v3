#!/usr/bin/python3
"""Module to handle state restful API actions"""

import models
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def state_all():
    """Retrives a list of all state objects"""
    states = models.storage.all('State')
    state_list = []
    for value in states.values():
        state_list.append(value.to_dict())
    return (jsonify(state_list))


@app_views.route('/states/<state_id>', methods=['GET'])
def state_grab(state_id):
    """grab one state based on ID"""
    states = models.storage.all('State')
    for key in states.keys():
        s, p, id = key.partition('.')
        if id == state_id:
            return (jsonify(states.get(key).to_dict()))
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def state_del(state_id):
    """delete a state object"""
    states = models.storage.all('State')
    for key in states.keys():
        s, p, id = key.partition('.')
        if id == state_id:
            models.storage.delete(states.get(key))
            models.storage.save()
            return (jsonify({}))
    abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def state_create():
    """Creates a state Object"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    name = request.get_json()
    state = models.state.State(**name)
    models.storage.new(state)
    models.storage.save()
    return (jsonify(state.to_dict()))


@app_views.route('/states/<state_id>', methods=['PUT'])
def state_change(state_id):
    """update a state object"""
    if not request.get_json():
        abort(400, "Not a JSON")
    states = models.storage.all('State')
    for key in states.keys():
        s, p, id = key.partition('.')
        if id == state_id:
            for k, v in request.get_json().items():
                if k not in ('id', 'created_at', 'updated_at'):
                    setattr(states[key], k, v)
            models.storage.save()
            return (jsonify(states[key].to_dict()))
    abort(404)
