#!/usr/bin/python3
"""Module to handle state restful API actions"""

import models
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def amenity_all():
    """Retrives a list of all amenities objects"""
    amenities = models.storage.all('Amenity')
    amenity_list = []
    for value in amenities.values():
        amenity_list.append(value.to_dict())
    return (jsonify(amenity_list))

@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenity_grab(amenity_id):
    """grab one amenity based on ID"""
    amenities = models.storage.all('Amenity')
    for key in amenities.keys():
        s, p, id = key.partition('.')
        if id == amenity_id:
            return (jsonify(amenities.get(key).to_dict()))
    abort(404)

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def amenity_del(amenity_id):
    """delete a amenity object"""
    amenities = models.storage.all('Amenity')
    for key in amenities.keys():
        s, p, id = key.partition('.')
        if id == amenity_id:
            models.storage.delete(amenities.get(key))
            models.storage.save()
            return (jsonify({}))
    abort(404)

@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def amenity_create():
    """Creates a amenity Object"""
    if not request.get_json():
         abort(400, "Not a JSON")
    if not 'name' in request.get_json():
         abort(400, "Missing name")
    name = request.get_json()
    amenity = models.amenity.Amenity(**name)
    models.storage.new(amenity)
    models.storage.save()
    return (jsonify(amenity.to_dict()))

@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def amenity_change(amenity_id):
    """update a amenity object"""
    if not request.get_json():
       abort(400, "Not a JSON")
    amenities = models.storage.all('Amenity')
    for key in amenities.keys():
        s, p, id = key.partition('.')
        if id == amenity_id:
            for k, v in request.get_json().items():
                if k not in ('id', 'created_at', 'updated_at'):
                    setattr(amenities[key], k, v) 
            models.storage.save()
            return (jsonify(amenities[key].to_dict()))
    abort(404)    
