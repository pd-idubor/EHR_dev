#!/usr/bin/python3
"""Links User and Medics objects and handles all default
    RestFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User
from models.medics import Medics
from os import environ


@app_views.route('/users/<user_id>/medics', methods=['GET'],
                 strict_slashes=False)
def get_user_medics(user_id):
    """Retrieves list of Medics objects of a User"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if environ.get('EHR_TYPE_STORAGE') == "db":
        medics = [medic.to_dict() for medic in user.medics]
    else:
        medics = [storage.get(Medics, medic_id).to_dict()
                     for medic_id in user.medic_ids]

    return jsonify(medics)


@app_views.route('/users/<user_id>/medics/<medic_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_plan(user_id, medic_id):
    """Deletes an Medics object to a User"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    medic = storage.get(Medics, medic_id)
    if medic is None:
        abort(404)

    if environ.get('EHR_TYPE_STORAGE') == "db":
        if medic not in user.medics:
            abort(404)
        user.medics.remove(medic)
    else:
        if medic_id not in user.medic_ids:
            abort(404)
        user.medic_ids.remove(medic_id)

    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users/<user_id>/medics/<medic_id>', methods=['POST'],
                 strict_slashes=False)
def link_plan(user_id, medic_id):
    """Link a Medics object to a User"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    medic = storage.get(Medics, medic_id)
    if medic is None:
        abort(404)

    if environ.get('EHR_TYPE_STORAGE') == "db":
        if medic in user.medics:
            return make_response(jsonify(medic.to_dict()), 200)
        else:
            user.medics.append(medic)
    else:
        if medic_id in user.medic_ids:
            return make_response(jsonify(medic.to_dict()), 200)
        else:
            user.medic_ids.append(medic_id)

    storage.save()
    return make_response(jsonify(medic.to_dict()), 201)
