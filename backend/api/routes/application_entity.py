from flask import request
from flask_restx import Resource, Namespace, fields

from api.models.user import User
from api.models.application_entity import ApplicationEntity 
from api.auth import verify_password

api = Namespace('Application Entity', description='Application Entities')

@api.route('/applicationentity', methods=['GET'])
class ApplicationEntityRoute(Resource):

    def get(self):
        return {'applicationentities': ApplicationEntity.Schema(many=True).dump(ApplicationEntity.query.all())}

