from flask_restx import Namespace, Resource

from api import config, docker
api = Namespace('containers', description='Container Control')


@api.route('/')
class ContainersRoute(Resource):

    def get(self):
        return {'containers': [c.attrs for c in docker.containers.list()]}
