#!/usr/bin/python3
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": ["0.0.0.0"]}})

@app.teardown_appcontext
def tear_down(exception):
    """Closes the current session"""
    storage.close()

@app.errorhandler(404)
def page_not_found(e):
    """Error handling, 404"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=os.getenv('EHR_API_HOST') or '0.0.0.0',
            port=int(os.getenv('EHR_API_PORT')) or 5000,
            threaded=True)
