from dataclasses import asdict

from flask_restx import Namespace, Resource, fields
from flask import request
from bson.objectid import ObjectId
from bson.errors import InvalidId

from api.encoders import jsonify
from api import db, socketio

from api.models import Job
from api.tasks.hello import count_words

api = Namespace('jobs', description='Background Tasks')


@api.route('/')
class JobsRoute(Resource):

    @api.response(200, 'Ok', Job.list_model())
    def get(self):
        socketio.emit('my_response', {'data': 'First emit'})
        return jsonify({'jobs': db.jobs.find()})

    @api.expect(Job.list_model())
    def post(self):
        # msg = count_words.send()
        job = Job('test', status='Queued', info='15 Second Test Func')
        print('Job', vars(job))
        _id = db.jobs.insert_one(vars(job)).inserted_id

        return jsonify(db.jobs.find_one({'_id': _id}))

    @api.response(200, 'Ok')
    def delete(self):
        return db.jobs.delete_many({}).deleted_count



