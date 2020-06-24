from dataclasses import asdict

from flask_restx import Namespace, Resource, fields
from flask import request
from bson.objectid import ObjectId
from bson.errors import InvalidId

from api.encoders import jsonify
from api import db

from dicom_tools.utils import Modality
from dicom_tools.echo import echo

api = Namespace('modalities', description='Modality Interaction')

modality = api.model('Modality', {'_id': fields.String, 'aet': fields.String, 'port': fields.Integer, 'address': fields.String})
modality_list = api.model('Modality List', {'modalities': fields.List(fields.Nested(modality))})


@api.errorhandler(InvalidId)
@api.header('My-Header',  'Some description')
def handel_invalid_oid(error):
    return {'message': str(error)}, 400, {'My-Header': 'Value'}


@api.route('/')
class ModalitiesRoute(Resource):

    @api.response(200, 'Ok', modality_list)
    def get(self):
        return jsonify({'modalities': db.modalities.find()})

    @api.expect(modality)
    def post(self):
        oid = db.modalities.insert_one(request.json).inserted_id
        return jsonify(db.modalities.find_one({'_id': oid}))


@api.route('/<string:modality_id>')
class ModalityRoute(Resource):

    @api.response(200, 'Ok', modality)
    @api.response(400, 'Not Ok')
    def get(self, modality_id):
        # raise InvalidId
        return jsonify(db.modalities.find_one({'_id': ObjectId(modality_id)}))

    @api.response(200, 'Deleted')
    def delete(self, modality_id):
        ret = db.modalities.delete_one({'_id': ObjectId(modality_id)})

        if not ret.deleted_count:
            return 'Can Not Delete', 501


@api.route('/<string:modality_id>/echo')
class ModalityEchoRoute(Resource):

    @api.response(500, 'Validation Error')
    def get(self, modality_id):
        try:
            oid = ObjectId(modality_id)
        except InvalidId:
            raise

        modality = db.modalities.find_one({'_id': oid}, {"_id": False})
        print(modality)

        echo(Modality(**modality))

