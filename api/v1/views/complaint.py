#!/usr/bin/python3
"""
    Handles default RESTFul API actions
"""
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.complaint import Complaint
from models.user import User
from models.diagnosis import Diagnosis


@app_views.route('/users/<user_id>/complaints', methods=['GET'],
                 strict_slashes=False)
def complaint(user_id=None):
    """Retrieves the list of all Complaint objects of a User"""
    if (user_id):
        user = storage.get("User", user_id)
        if user is not None:
            complaints = [complaint.to_dict() for complaint in user.complaints]
            return jsonify(complaints)
        abort(404)


@app_views.route('/complaints/<complaint_id>', methods=['GET'],
                 strict_slashes=False)
def get_complaint(complaint_id=None):
    """Retrieves Complaint objects"""
    if (complaint_id):
        complaint = storage.get("Complaint", complaint_id)
        if complaint is not None:
            return jsonify(complaint.to_dict())
        abort(404)


@app_views.route('/complaints/<complaint_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_complaint(complaint_id=None):
    """Deletes a Complaint object"""
    if (complaint_id):
        complaint = storage.get("Complaint", complaint_id)
        if complaint is not None:
            storage.delete(complaint)
            storage.save()
            return (jsonify({}), 200)
        abort(404)


@app_views.route('/users/<user_id>/complaints', methods=["POST"],
                 strict_slashes=False)
def create_complaint(user_id=None):
    """Creates a Complaint"""
    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)

    event = data.get("event")
    if event is None:
        return (jsonify({"error": "Missing event"}), 400)

    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    diagnosis_id = data.get("diagnosis_id")
    if diagnosis_id is None:
        return (jsonify({"error": "Missing diagnosis_id"}), 400)

    diagnosis = storage.get("Diagnosis", diagnosis_id)
    if diagnosis is None:
        abort(404)

    text = data.get("text")
    if text is None:
        return (jsonify({"error": "Missing text"}), 400)

    new = Complaint()
    new.user_id = user.id

    for key, val in data.items():
        setattr(new, key, val)
    new.save()
    return (jsonify(new.to_dict()), 201)


@app_views.route('/complaints/<complaint_id>', methods=["PUT"],
                 strict_slashes=False)
def update_complaint(complaint_id):
    """Updates a Complaint"""
    complaint = storage.get("Complaint", complaint_id)
    if complaint is None:
        abort(404)

    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)

    ignore = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore:
            setattr(complaint, key, value)

    complaint.save()
    return (jsonify(complaint.to_dict()), 200)
