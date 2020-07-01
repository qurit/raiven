from dataclasses import asdict

from flask_restx import Namespace, Resource, fields, Model
from flask import request
from bson.objectid import ObjectId
from bson.errors import InvalidId

from api.encoders import jsonify
from api import db, socketio

from api.models import Job, BaseModel
from api.tasks.hello import count_words

api = Namespace('jobs', description='Background Tasks')


job_schema = Job.model()
job_list_schema = Job.list_model()
api.add_model(name=job_schema.name, definition=job_schema)
api.add_model(name=job_list_schema.name, definition=job_list_schema)


@api.route('/')
class JobsRoute(Resource):

    @api.response(200, 'Ok', job_list_schema)
    def get(self):
        socketio.emit('my_response', {'data': 'First emit'})
        return jsonify({'jobs': db.jobs.find()})

    @api.expect(job_schema)
    def post(self):
        msg = count_words.send()
        job = Job(msg.message_id,  status='Queued', info='15 Second Test Func').insert()
        return jsonify(vars(job))

    @api.response(200, 'Ok')
    def delete(self):
        return db.jobs.delete_many({}).deleted_count

