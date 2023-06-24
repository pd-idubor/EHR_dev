#!/usr/bin/python3
"""
    Handles default RESTFul API actions
"""
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from models.diagnosis import Diagnosis


@app_views.route('/users/<user_id>/diags', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/users/<user_id>', methods=["GET"], strict_slashes=False)
def diags_by_users(user_id=None):
    """Retrieves the list of all Diagnosis objects of a User"""
    if (user_id):
        user = storage.get("User", user_id)
        if user is not None:
            diags = [diag.to_dict() for diag in user.diags]
            return jsonify(diags)
        abort(404)


@app_views.route('/diags/<diag_id>', methods=['GET'],
                 strict_slashes=False)
def get_diag(diag_id=None):
    """Retrieves Diagnosis objects"""
    if (diag_id):
        diag = storage.get("Diagnosis", diag_id)
        if diag is not None:
            return jsonify(diag.to_dict())
        abort(404)


@app_views.route('/diags/<diag_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_diags(diag_id=None):
    """Deletes a Diagnosis object"""
    if (diag_id):
        diag = storage.get("Diagnosis", diag_id)
        if diag is not None:
            storage.delete(diag)
            storage.save()
            return (jsonify({}), 200)
        abort(404)


@app_views.route('/users/<user_id>/diags', methods=["POST"],
                 strict_slashes=False)
def post_diags(user_id=None):
    """Creates a Diagnosis"""
    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)
    name = data.get("name")
    if name is None:
        return (jsonify({"error": "Missing name"}), 400)

    user = storage.get("User", user_id)
    if user is not None:
        new_diag = Diagnosis()
        new_diag.user_id = user_id
        new_diag.name = name
        new_diag.save()
        return (jsonify(new_diag.to_dict()), 201)
    abort(404)


@app_views.route('diags/<diag_id>', methods=["PUT"],
                 strict_slashes=False)
def update_diags(diag_id):
    """Updates a Diagnosis"""
    diag = storage.get("Diagnosis", diag_id)
    if diag is None:
        abort(404)

    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)

    ignore = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore:
            setattr(diag, key, value)

    diag.save()
    return (jsonify(diag.to_dict()), 200)
