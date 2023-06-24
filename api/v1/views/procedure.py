#!/usr/bin/python3
"""
    Handles default RESTFul API actions
"""
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.procedure import Procedure


@app_views.route('/procs', methods=['GET'], strict_slashes=False)
@app_views.route('/procs/<proc_id>', methods=["GET"],
                 strict_slashes=False)
def all_procs(proc_id=None):
    """Retrieves the list of all Procedure objects"""
    if (proc_id):
        proc = storage.get("Procedure", proc_id)
        if proc is not None:
            return jsonify(proc.to_dict())
        abort(404)

    new_list = []
    procs = storage.all("Procedure")
    for proc in procs.values():
        new_list.append(proc.to_dict())
    return jsonify(new_list)


@app_views.route('/procs/<proc_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_procs(proc_id=None):
    """Deletes an Procedure  object"""
    if (proc_id):
        proc = storage.get("Procedure", proc_id)
        if proc is not None:
            storage.delete(proc)
            storage.save()
            return (jsonify({}))
        abort(404)


@app_views.route('/procs', methods=["POST"],
                 strict_slashes=False)
def create_procs():
    """Creates a Procedure"""
    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)
    name = data.get("name")
    if name is None:
        return (jsonify({"error": "Missing name"}), 400)

    new = Procedure()
    new.name = name
    new.save()
    return (jsonify(new.to_dict()), 201)


@app_views.route('/procs/<proc_id>', methods=["PUT"],
                 strict_slashes=False)
def update_procs(proc_id):
    """Updates a Procedure"""
    proc = storage.get("Procedure", proc_id)
    if proc is None:
        abort(404)

    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)

    ignore = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore:
            setattr(proc, key, value)

    proc.save()
    return (jsonify(proc.to_dict()), 200)
