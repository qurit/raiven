from flask import request
from flask_restx import Resource, Namespace, fields

from api.models.user import User
from api.models.application_entity import ApplicationEntity 
from api.auth import verify_password

api = Namespace('Auth', description='User Authentication')
login_model = api.model('Auth', {'username': fields.String, 'password': fields.String})


@api.route('/login', methods=['POST'])
class LoginRoute(Resource):

    @api.expect(login_model)
    def post(self):
        data = request.json
        username = data['username']
        password = data['password']

        user = verify_password(username, password)
        if not user:
            return 'Unauthorized', 401

        return user, 200


@api.route('/users', methods=['GET'])
class UsersRoute(Resource):

    def get(self):
        return {'users': User.Schema(many=True).dump(User.query.all())}

@api.route('/applicationentity', methods=['GET'])
class ApplicationEntityRoute(Resource):

    def get(self):
        return {'applicationentities': ApplicationEntity.Schema(many=True).dump(ApplicationEntity.query.all())}

