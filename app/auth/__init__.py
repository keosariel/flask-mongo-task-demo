from flask import Blueprint
from flask_restful import Api

from .resources import Login, Register

auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)

api.add_resource(Login, "/login")
api.add_resource(Register, "/register")