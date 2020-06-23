from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import Flask, request
from flask_restplus import Resource, Api
from flask_pymongo import PyMongo
from flask_cors import CORS

from dicom import echo, utils

from api.encoders import jsonify

from config import BaseConfig
config = BaseConfig()

app = Flask(__name__)
app.config.from_object(config)
CORS(app, resources={r'/*': {'origins': '*'}})

api = Api(app)
mongo = PyMongo(app)
db = mongo.db


@api.route('/hello')
class HelloWorld(Resource):

    def get(self):
        mongo.db.modalities.insert_one({'aet': 'MIT', 'port': 4000, 'address': 'localhost'})
        return {'hello': 'world'}


@api.route('/modalities')
class Modalities(Resource):

    def get(self):
        print()
        return jsonify({'modalities': db.modalities.find()})

    def post(self):
        oid = db.modalities.insert_one(request.json).inserted_id
        return jsonify(db.modalities.find_one({'_id': oid}))


@api.route('/modalities/<string:modality_id>')
class Modality(Resource):

    def get(self):
        return jsonify({'modalities': db.modalities.find()})

    def delete(self, modality_id):
        ret = db.modalities.delete_one({'_id': ObjectId(modality_id)})

        if ret.deleted_count:
            return 'Deleted', 200
        else:
            return 'Can Not Delete', 501


@api.route('/dicom/echo/<string:modality_id>')
class Echo(Resource):

    def get(self, modality_id):
        oid = ObjectId(modality_id)
        modality = db.modalities.find_one({'_id': oid}, {"_id": False})
        print(modality)
        md = utils.Modality(**modality)

        return 'Not implemented', 501
