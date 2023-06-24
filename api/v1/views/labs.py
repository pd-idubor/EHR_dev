#!/usr/bin/python3
"""
    Handles default RESTFul API actions
"""
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from models.labs import Labs


@app_views.route('/users/<user_id>/labs', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/users/<user_id>', methods=["GET"], strict_slashes=False)
def labs_by_users(user_id=None):
    """Retrieves the list of all Labs objects of a User"""
    if (user_id):
        user = storage.get("User", user_id)
        if user is not None:
            labs = [lab.to_dict() for lab in user.labs]
            return jsonify(labs)
        abort(404)


@app_views.route('/labs/<lab_id>', methods=['GET'],
                 strict_slashes=False)
def get_lab(lab_id=None):
    """Retrieves Labs objects"""
    if (lab_id):
        lab = storage.get("Labs", lab_id)
        if lab is not None:
            return jsonify(lab.to_dict())
        abort(404)


@app_views.route('/labs/<lab_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_labs(lab_id=None):
    """Deletes a Labs object"""
    if (lab_id):
        lab = storage.get("Labs", lab_id)
        if lab is not None:
            storage.delete(lab)
            storage.save()
            return (jsonify({}), 200)
        abort(404)


@app_views.route('/users/<user_id>/labs', methods=["POST"],
                 strict_slashes=False)
def post_labs(user_id=None):
    """Creates a Labs"""
    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)
    name = data.get("name")
    if name is None:
        return (jsonify({"error": "Missing name"}), 400)

    user = storage.get("User", user_id)
    if user is not None:
        new_lab = Labs()
        new_lab.user_id = user_id
        new_lab.name = name
        new_lab.save()
        return (jsonify(new_lab.to_dict()), 201)
    abort(404)


@app_views.route('labs/<lab_id>', methods=["PUT"],
                 strict_slashes=False)
def update_labs(lab_id):
    """Updates a Labs"""
    lab = storage.get("Labs", lab_id)
    if lab is None:
        abort(404)

    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)

    ignore = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore:
            setattr(lab, key, value)

    lab.save()
    return (jsonify(lab.to_dict()), 200)
