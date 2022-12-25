"""
Journals api 
"""
from flask import Blueprint, request, jsonify

from libraryapi.models import Journal

journals = Blueprint("journals", __name__, url_prefix="/api/v1/")


@journals.get('/journals/')
def fetch_journals():
    journals = Journal.query.all()
    return jsonify([journal.to_dict() for journal in journals])
