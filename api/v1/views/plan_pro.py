#!/usr/bin/python3
"""Links User and Procedure objects and handles all default
    RestFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User
from models.procedure import Procedure
from os import environ


@app_views.route('/users/<user_id>/procs', methods=['GET'],
                 strict_slashes=False)
def get_user_procs(user_id):
    """Retrieves list of Procedure objects of a User"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if environ.get('EHR_TYPE_STORAGE') == "db":
        procs = [proc.to_dict() for proc in user.procs]
    else:
        procs = [storage.get(Procedure, proc_id).to_dict()
                     for proc_id in user.proc_ids]

    return jsonify(procs)


@app_views.route('/users/<user_id>/procs/<proc_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_plan(user_id, proc_id):
    """Deletes an Procedure object to a User"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    proc = storage.get(Procedure, proc_id)
    if proc is None:
        abort(404)

    if environ.get('EHR_TYPE_STORAGE') == "db":
        if proc not in user.procs:
            abort(404)
        user.procs.remove(proc)
    else:
        if proc_id not in user.proc_ids:
            abort(404)
        user.proc_ids.remove(proc_id)

    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users/<user_id>/procs/<proc_id>', methods=['POST'],
                 strict_slashes=False)
def link_plan(user_id, proc_id):
    """Link a Procedure object to a User"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    proc = storage.get(Procedure, proc_id)
    if proc is None:
        abort(404)

    if environ.get('EHR_TYPE_STORAGE') == "db":
        if proc in user.procs:
            return make_response(jsonify(proc.to_dict()), 200)
        else:
            user.procs.append(proc)
    else:
        if proc_id in user.proc_ids:
            return make_response(jsonify(proc.to_dict()), 200)
        else:
            user.proc_ids.append(proc_id)

    storage.save()
    return make_response(jsonify(proc.to_dict()), 201)
