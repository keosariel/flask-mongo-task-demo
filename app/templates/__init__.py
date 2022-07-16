from flask import Blueprint
from flask_restful import Api

from .resources import Template

template_bp = Blueprint('template', __name__)
api = Api(template_bp, prefix='/template')


api.add_resource(Template, '/', '/<string:template_id>')