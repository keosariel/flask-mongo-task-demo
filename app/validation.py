from flask import request, jsonify
from functools import wraps

from .models import Users

register_schema = {
    'type': 'object',
    'properties': {
        'first_name': {'type': 'string'},
        'last_name': {'type': 'string'},
        'email': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['first_name', 'last_name','email', 'password']
}

login_schema = {
    'type': 'object',
    'properties': {
        'email': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['email', 'password']
}


template_schema = {
    'type': 'object',
    'properties': {
        'template_name': {'type': 'string'},
        'subject': {'type': 'string'},
        'body': {'type': 'string'}
    },
    'required': ['template_name', 'subject', 'body']
}



def login_required():
    """
    Checks and validates the Authorization Header `Bearer Token`    
    if token is valid it'd set the `current_user`
    """

    def _login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token_error = {"error": "Invalid or expired token"}

            try:
                auth_header = request.headers.get('Authorization')
                token = auth_header.split(" ")[1]
            except Exception:
                return token_error, 401

            is_valid, user_id = Users.decode_token(token.strip())
            if not is_valid:
                return token_error, 401
            
            user = Users._from("_id", user_id)

            if not user:
                return {"error": "User does not exists"}, 404
            else:
                return f(*args, **kwargs, current_user=user)

        return decorated_function

    return _login_required