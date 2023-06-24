#!/usr/bin/python3
"""
    Handles default RESTFul API actions
"""
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.practitioner import Practitioner


@app_views.route('/practitioners', methods=['GET'], strict_slashes=False)
@app_views.route('/practitioners/<practitioner_id>', methods=["GET"], strict_slashes=False)
def all_practitioners(practitioner_id=None):
    """Retrieves the list of all Practitioner objects"""
    if (practitioner_id):
        practitioner = storage.get("Practitioner", practitioner_id)
        if practitioner is not None:
            return jsonify(practitioner.to_dict())
        abort(404)

    new_list = []
    practitioners = storage.all("Practitioner")
    for practitioner in practitioners.values():
        new_list.append(practitioner.to_dict())
    return jsonify(new_list)


@app_views.route('/practitioners/<practitioner_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_practitioners(practitioner_id=None):
    """Deletes a Practitioner object"""
    if (practitioner_id):
        practitioner = storage.get("Practitioner", practitioner_id)
        if practitioner is not None:
            storage.delete(practitioner)
            storage.save()
            return (jsonify({}), 200)
        abort(404)


@app_views.route('/practitioners', methods=["POST"],
                 strict_slashes=False)
def create_practitioners():
    """Creates a Practitioner"""
    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)
    email = data.get("email")
    if email is None:
        return (jsonify({"error": "Missing email"}), 400)
    password = data.get("password")
    if password is None:
        return (jsonify({"error": "Missing password"}), 400)
    practice = data.get("practice")
    if practice is None:
        return (jsonify({"error": "Missing practice"}), 400)
    license = data.get("license")
    if license is None:
        return (jsonify({"error": "Missing license"}), 400)
    if name = data.get("name")
    if name is None:
        retrun (jsonify({"error": "Missing name"}), 400)

    new = Practitioner()
    for key, value in data.items():
        setattr(new, key, value)
    new.save()
    return (jsonify(new.to_dict()), 201)


@app_views.route('/practitioners/<practitioner_id>', methods=["PUT"],
                 strict_slashes=False)
def update_practitioners(practitioner_id):
    """Updates a Practitioner"""
    practitioner = storage.get("Practitioner", practitioner_id)
    if practitioner is None:
        abort(404)

    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)

    ignore = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore:
            setattr(practitioner, key, value)

    practitioner.save()
    return (jsonify(practitioner.to_dict()), 200)
