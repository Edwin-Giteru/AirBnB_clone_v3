#!/usr/bin/python3

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def closes_storage(exc=None):
    """closes storage"""
    storage.close()

@app.errorhandler(404)
def not_found(exc=None):
    """handles not found error"""
    response = jsonify(error='Not Found')
    response.status_code = 404
    return response

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST') if os.getenv('HBNB_API_HOST') is not None else '0.0.00'
    port = os.getenv('HBNB_API_PORT') if os.getenv('HBNB_API_PORT') is not None else 5000
    app.run(threaded =True, host=host, port=port)
