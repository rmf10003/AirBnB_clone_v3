#!/usr/bin/python3
"""Module to handle state restful API actions"""

import models
from flask import Flask, jsonify, request, abort, make_response
from api.v1.views import app_views


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def user_all():
    """Retrives a list of all users objects"""
    users = models.storage.all('User')
    user_list = []
    for value in users.values():
        user_list.append(value.to_dict())
    return (jsonify(user_list))


@app_views.route('/users/<user_id>', methods=['GET'])
def user_grab(user_id):
    """grab one user based on ID"""
    users = models.storage.all('User')
    for key in users.keys():
        s, p, id = key.partition('.')
        if id == user_id:
            return (jsonify(users.get(key).to_dict()))
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def user_del(user_id):
    """delete a user object"""
    users = models.storage.all('User')
    for key in users.keys():
        s, p, id = key.partition('.')
        if id == user_id:
            models.storage.delete(users.get(key))
            models.storage.save()
            return (jsonify({}))
    abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def user_create():
    """Creates a user Object"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'email' not in request.get_json():
        abort(400, "Missing email")
    if 'password' not in request.get_json():
        abort(400, "Missing password")
    name = request.get_json()
    user = models.user.User(**name)
    models.storage.new(user)
    models.storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def user_change(user_id):
    """update a user object"""
    if not request.get_json():
        abort(400, "Not a JSON")
    users = models.storage.all('User')
    for key in users.keys():
        s, p, id = key.partition('.')
        if id == user_id:
            for k, v in request.get_json().items():
                if k not in ('email', 'id', 'created_at', 'updated_at'):
                    setattr(users[key], k, v)
            models.storage.save()
            return (jsonify(users[key].to_dict()))
    abort(404)
