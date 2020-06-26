from flask import request
from flask_restx import Resource, Namespace, fields

from api.models import user as user_model
from api.auth import verify_password

api = Namespace('user', description='User Auth')
user_model = api.model(*user_model)
user_list_model = api.model('Job List', {'jobs': fields.List(fields.Nested(user_model))})

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
