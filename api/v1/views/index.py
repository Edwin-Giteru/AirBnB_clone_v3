#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status')
def status():
    """check staus"""
    return jsonify(status='OK')

@app_views.route('/api/v1/stats')
def stats():
    """check stats"""
    return jsonify(storage.count())
