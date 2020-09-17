from flask import request
from flask_restx import Resource, Namespace, fields

from api.models.user import User
from api.auth import verify_password

api = Namespace('Auth', description='User Authentication')
login_model = api.model('Auth', {'username': fields.String, 'password': fields.String})


@api.route('/login', methods=['POST'])
class LoginRout(Resource):

    @api.expect(login_model)
    def post(self):
        data = request.json
        username = data['username']
        password = data['password']

        user = verify_password(username, password)
        if not user:
            return 'Unauthorized', 401

        return user, 200
