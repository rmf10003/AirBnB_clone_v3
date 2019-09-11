#!/usr/bin/python3
"""Module for api"""

from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, origins='0.0.0.0')


@app.teardown_appcontext
def teardown(self):
    """Method to close storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Custom error handler"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    app.run(
        host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
        port=os.getenv('HBNB_API_PORT', '5000'),
        threaded=True)
