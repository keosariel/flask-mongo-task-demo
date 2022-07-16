from flask import request
from flask_restful import Resource
from flask_expects_json import expects_json

from app.validation import template_schema, login_required
from app.models import Templates

class Template(Resource):

    @expects_json(template_schema)
    @login_required()
    def post(self, current_user):
        """Creates a new template"""
        template = Templates(
            template_name=request.json.get("template_name"),
            subject=request.json.get("subject"),
            body=request.json.get("body"),
            user_id=current_user._id
        )

        template.save()
        
        return template.to_dict, 201

    @login_required()
    def get(self, current_user, template_id=None):
        """Gets a template with the `template_id`"""
        if template_id:
            template = Templates._from("_id", template_id)

            if not template:
                return {"error": "Template not found"}, 404
            
            if current_user._id != template.user_id:
                return {"error": "User cannot access resource"}, 401

            return template.to_dict

        return Templates.all(user_id=current_user._id)


    @expects_json(template_schema)
    @login_required()
    def put(self, current_user, template_id):
        """Edit/Updates a template with the `template_id`"""
        template = Templates._from("_id", template_id)

        if not template:
            return {"error": "Template not found"}, 404
        
        if current_user._id != template.user_id:
            return {"error": "User cannot modify resource"}, 401

        template.template_name = request.json.get("template_name") or template.template_name
        template.subject = request.json.get("subject") or template.subject
        template.body = request.json.get("body") or template.body

        template.update()
        
        return template.to_dict, 201

    @login_required()
    def delete(self, current_user, template_id):
        """Deletes a template with the `template_id`"""
        template = Templates._from("_id", template_id)

        if not template:
            return {"error": "Template not found"}, 404
        
        if current_user._id != template.user_id:
            return {"error": "User cannot modify resource"}, 401

        template.delete()

        return {}, 201
