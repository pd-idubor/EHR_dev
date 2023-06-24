#!/usr/bin/python3
"""
    Handles default RESTFul API actions
"""
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from models.demo import Demo


@app_views.route('/users/<user_id>/demos', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/users/<user_id>', methods=["GET"], strict_slashes=False)
def demos_by_users(user_id=None):
    """Retrieves the list of all Demo objects of a User"""
    if (user_id):
        user = storage.get("User", user_id)
        if user is not None:
            demos = [demo.to_dict() for demo in user.demos]
            return jsonify(demos)
        abort(404)


@app_views.route('/demos/<demo_id>', methods=['GET'],
                 strict_slashes=False)
def get_demo(demo_id=None):
    """Retrieves Demo objects"""
    if (demo_id):
        demo = storage.get("Demo", demo_id)
        if demo is not None:
            return jsonify(demo.to_dict())
        abort(404)


@app_views.route('/demos/<demo_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_demos(demo_id=None):
    """Deletes a Demo object"""
    if (demo_id):
        demo = storage.get("Demo", demo_id)
        if demo is not None:
            storage.delete(demo)
            storage.save()
            return (jsonify({}), 200)
        abort(404)


@app_views.route('/users/<user_id>/demos', methods=["POST"],
                 strict_slashes=False)
def post_demos(user_id=None):
    """Creates a Demo"""
    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)
    gender = data.get("gender")
    if gender is None:
        return (jsonify({"error": "Missing gender"}), 400)

    user = storage.get("User", user_id)
    if user is not None:
        new_demo = Demo()
        new_demo.user_id = user_id
        new_demo.gender = gender
        new_demo.save()
        return (jsonify(new_demo.to_dict()), 201)
    abort(404)


@app_views.route('demos/<demo_id>', methods=["PUT"],
                 strict_slashes=False)
def update_demos(demo_id):
    """Updates a Demo"""
    demo = storage.get("Demo", demo_id)
    if demo is None:
        abort(404)

    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)

    ignore = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore:
            setattr(demo, key, value)

    demo.save()
    return (jsonify(demo.to_dict()), 200)
