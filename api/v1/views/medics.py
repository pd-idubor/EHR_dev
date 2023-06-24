#!/usr/bin/python3
"""
    Handles default RESTFul API actions
"""
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.medics import Medics


@app_views.route('/medics', methods=['GET'], strict_slashes=False)
@app_views.route('/medics/<medic_id>', methods=["GET"],
                 strict_slashes=False)
def all_medics(medic_id=None):
    """Retrieves the list of all Medics objects"""
    if (medic_id):
        medic = storage.get("Medics", medic_id)
        if medic is not None:
            return jsonify(medic.to_dict())
        abort(404)

    new_list = []
    medics = storage.all("Medics")
    for medic in medics.values():
        new_list.append(medic.to_dict())
    return jsonify(new_list)


@app_views.route('/medics/<medic_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_medics(medic_id=None):
    """Deletes an Medics  object"""
    if (medic_id):
        medic = storage.get("Medics", medic_id)
        if medic is not None:
            storage.delete(medic)
            storage.save()
            return (jsonify({}))
        abort(404)


@app_views.route('/medics', methods=["POST"],
                 strict_slashes=False)
def create_medics():
    """Creates a Medic"""
    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)
    name = data.get("name")
    if name is None:
        return (jsonify({"error": "Missing name"}), 400)

    new = Medics()
    new.name = name
    new.save()
    return (jsonify(new.to_dict()), 201)


@app_views.route('/medics/<medic_id>', methods=["PUT"],
                 strict_slashes=False)
def update_medics(medic_id):
    """Updates a Med"""
    medic = storage.get("Medics", medic_id)
    if medic is None:
        abort(404)

    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)

    ignore = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore:
            setattr(medic, key, value)

    medic.save()
    return (jsonify(medic.to_dict()), 200)
