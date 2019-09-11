#!/usr/bin/python3
"""Module to handle state restful API actions"""

import models
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def all_states():
    """Retrives a list of all state objects"""
    states = models.storage.all('State')
    state_list = []
    for value in states.values():
        state_list.append(value.to_dict())
    return (jsonify(state_list))

@app_views.route('/states/<state_id>', methods=['GET'])
def grab_state(state_id):
    """grab one state based on ID"""
    states = models.storage.all('State')
    for key in states.keys():
        s, p, id = key.partition('.')
        if id == state_id:
            return (jsonify(states.get(key).to_dict()))
    abort(404)

@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_state(state_id):
    """delete a state object"""
    states = models.storage.all('State')
    for key in states.keys():
        s, p, id = key.partition('.')
        if id == state_id:
            models.storage.delete(states.get(key))
            models.storage.save()
            return (jsonify({}))
    abort(404)
