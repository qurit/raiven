from flask import request
from flask_restx import Namespace, Resource, fields

from docker.types.services import ServiceMode

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
        print(docker.services.list(filters={'name': 'picom_worker'}))
        s = docker.services.list(filters={'name': 'picom_worker'})[0]
        print(s)

        print(request.json)
        count = request.json['count']
        count = int(count)

        print(f'SCALING SERVICE {s.name} TO {count}')
        s.scale(count)
        print('SCALED!')
        return 'Ok'

    def get(self):
        return {'workers': [c.attrs for c in docker.containers.list() if '/picom_worker' in c.attrs['Name']]}


if __name__ == '__main__':
    s = docker.services.list()
    print(s)

    for ser in s:
        print(ser.attrs)
#        ser.Soec.Name

