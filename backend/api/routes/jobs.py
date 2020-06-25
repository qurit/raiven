from dataclasses import asdict

from flask_restx import Namespace, Resource, fields
from flask import request
from bson.objectid import ObjectId
from bson.errors import InvalidId

from api.encoders import jsonify
from api import db, socketio

from api.models import job
from api.tasks.hello import count_words

api = Namespace('jobs', description='Background Tasks')
job_model = api.model(*job)
job_list_model = api.model('Job List', {'jobs': fields.List(fields.Nested(job_model))})


@api.route('/')
class JobsRoute(Resource):

    @api.response(200, 'Ok', job_list_model)
    def get(self):
        socketio.emit('my_response', {'data': 'First emit'})
        return jsonify({'jobs': db.jobs.find()})

    @api.expect(job_list_model)
    def post(self):
        msg = count_words.send()
        _id = db.jobs.insert_one({'pid': msg.message_id, 'status': 'Queued', 'info': '15 Second Test Func'}).inserted_id
        return jsonify(db.jobs.find_one({'_id': _id}))

    @api.response(200, 'Ok')
    def delete(self):
        return db.jobs.delete_many({}).deleted_count



