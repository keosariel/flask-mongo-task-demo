from datetime import datetime, timedelta
from flask import current_app
import jwt
import uuid

from . import mongo, bcrypt

class Users:
    collection = mongo.db.users

    def __init__(self, first_name, last_name, email, password, _id=None, exists=False):
        """Creates a new user

        Args:
            first_name (str): user's first name
            last_name (str): user's last name
            email (str): user's unique email
            password (str): user's password
            _id (str): unique id for user 
            exists (bool): if False create a new user else just load user object

        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self._id = _id or str(uuid.uuid4())

        if not exists:
            self.password = bcrypt.generate_password_hash(password).decode()
        else:
            self.password = password

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return bcrypt.check_password_hash(self.password, password)

    def generate_token(self, hours=24):
        """Generates the access token"""

        # set up a payload with an expiration time
        payload = {
            'exp': datetime.utcnow() + timedelta(hours=hours),
            'iat': datetime.utcnow(),
            'sub': self._id
        }
        # create the byte string token using the payload and the SECRET key
        jwt_string = jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )

        if type(jwt_string) == bytes:
            jwt_string = jwt_string.decode()

        return jwt_string

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config.get(
                'SECRET_KEY'), algorithms=['HS256'])
            return True, payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return False, "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return False, "Invalid token. Please register or login"

        return False, "Invalid token. Please register or login"

    def auth_details(self):
        return {"access_token":self.generate_token(), "user": self.to_dict}

    @staticmethod
    def _from(key, value):
        """Get an item base on the `key` and `value` given
        
        Args:
            key (str): target
            value (any): target's value
        
        Returns: 
            A user object if anyone found else `None`
        """
        user_dict = Users.collection.find_one({key: value})
        if user_dict:
            user = Users(**user_dict, exists=True)
            return user

    @property
    def to_dict(self):
        """Returns a dictionary represention of the `users` object"""
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "_id": self._id
        }

    def save(self):
        """Saves a user object"""
        self.collection.insert_one({**self.to_dict, "password":self.password})


class Templates:

    collection = mongo.db.templates

    def __init__(self, template_name, subject, body, user_id, _id=None):
        """Creates a new template"""

        self.template_name = template_name
        self.subject = subject
        self.body = body
        self._id = _id or str(uuid.uuid4())
        self.user_id = user_id

    @property
    def to_dict(self):
        """Returns a dictionary represention of the `templates` object"""
        return {
            "template_name": self.template_name,
            "subject": self.subject,
            "body": self.body,
            "_id": self._id,
            "user_id": self.user_id
        }
    
    @staticmethod
    def _from(key, value):
        """Get an item base on the `key` and `value` given
        
        Args:
            key (str): target
            value (any): target's value
        
        Returns: 
            A user object if anyone found else `None`
        """
        template_dict = Templates.collection.find_one({key: value})
        if template_dict:
            template = Templates(**template_dict)
            return template

    def update(self):
        """Updates template with the current set properties"""
        data = self.to_dict
        data.pop("_id")

        return self.collection.update_one(
            {"_id": self._id},
            {"$set": self.to_dict}
        )

    def delete(self):
        """Deletes a template"""
        return self.collection.delete_one({"_id": self._id})

    def save(self):
        """Saves templates"""
        self.collection.insert_one({**self.to_dict})

    @staticmethod
    def all(user_id):
        """Get all templates for `user_id`"""
        return list(Templates.collection.find({"user_id": user_id}))
