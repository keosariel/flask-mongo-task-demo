from flask import request, jsonify
from flask_restful import Resource
from flask_expects_json import expects_json

from app.validation import register_schema, login_schema
from app.models import Users

class Register(Resource):

    @expects_json(register_schema)
    def post(self):
        """Registers a new user"""
        user = Users._from("email", request.json.get("email"))

        if user:
            return {"error": "Email already exists!"}, 400

        user = Users(
            first_name=request.json.get("first_name"),
            last_name=request.json.get("last_name"),
            email=request.json.get("email"),
            password=request.json.get("password"),
        )

        user.save()
        return user.auth_details(), 201


class Login(Resource):

    @expects_json(login_schema)
    def post(self):
        """Login an existing user"""
        user = Users._from("email", request.json.get("email"))
        if user.password_is_valid(request.json.get("password")):
            return user.auth_details()
        
        return {"error": "invalid email or password"}, 401
        