#!/usr/bin/python3
"""Module to handle review restful API actions"""

import models
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False,
                 methods=['GET'])
def review_all(place_id):
    """Retrives a list of all review objects"""
    places = models.storage.all('Place')
    place_key = 'Place.' + place_id
    review_list = []
    if place_key in places.keys():
        place = places.get(place_key)
    else:
        abort(404)
    for review in place.reviews:
        review_list.append(review.to_dict())
    return(jsonify(review_list))


@app_views.route('/reviews/<review_id>', methods=['GET'])
def review_grab(review_id):
    """grab one review based on ID"""
    reviews = models.storage.all('Review')
    for key in reviews.keys():
        c, p, id = key.partition('.')
        if id == review_id:
            return (jsonify(reviews.get(key).to_dict()))
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def review_del(review_id):
    """delete a review object"""
    reviews = models.storage.all('Review')
    for key in reviews.keys():
        s, p, id = key.partition('.')
        if id == review_id:
            models.storage.delete(reviews.get(key))
            models.storage.save()
            return (jsonify({}))
    abort(404)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False,
                 methods=['POST'])
def review_create(place_id):
    """Creates a review Object"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    places = models.storage.all('Place')
    place_key = 'Place.' + place_id
    review_list = []
    if place_key not in places.keys():
        abort(404)
    name = request.get_json()
    review = models.review.Review(place_id=place_id, **name)
    models.storage.new(review)
    models.storage.save()
    return (jsonify(review.to_dict()))


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def review_change(review_id):
    """update a review object"""
    if not request.get_json():
        abort(400, "Not a JSON")
    reviews = models.storage.all('Review')
    for key in reviews.keys():
        s, p, id = key.partition('.')
        if id == review_id:
            for k, v in request.get_json().items():
                if k not in ('id', 'place_id', 'created_at', 'updated_at'):
                    setattr(reviews[key], k, v)
            models.storage.save()
            return (jsonify(reviews[key].to_dict()))
    abort(404)
