"""
Journals api 
"""
from flask import Blueprint, request, jsonify

journals = Blueprint("journals", __name__, url_prefix="/api/v1/")


@journals.get('/journals/')
def fetch_journals():
    return jsonify({"journals": "journal 1"})
