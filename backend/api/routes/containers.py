from flask import request
from flask_restx import Namespace, Resource, fields


from api import config, docker
api = Namespace('containers', description='Container Control')


@api.route('/')
class ContainersRoute(Resource):

    def get(self):
        return {'containers': [c.attrs for c in docker.containers.list()]}


@api.route('/workers')
class WorkersRoute(Resource):

    @api.expect({'count': fields.Integer})
    def post(self):
        data = request.json
        docker.containers.run(
            'picom_worker',
            command='dramatiq api --watch .',
            network='picom_default',
            remove=True,
        )

    def get(self):
        return {'workers': [c.attrs for c in docker.containers.list() if '/picom_worker' in c.attrs['Name']]}
