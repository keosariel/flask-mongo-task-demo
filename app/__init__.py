from flask import Flask, jsonify, make_response
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
from jsonschema import ValidationError

from .config import Config

app = Flask(__name__)
app.config.from_object(Config)
bcrypt = Bcrypt(app)
mongo = PyMongo(app)

from .auth import auth_bp
from .templates import template_bp

app.register_blueprint(auth_bp)
app.register_blueprint(template_bp)

@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(jsonify({'error': original_error.message}), 400)
    # handle other "Bad Request"-errors
    return error