from flask import request
from flask_restx import Resource, Namespace, fields

from api.models.application_entity import ApplicationEntity 
# from api.models.dicom_patient import DicomPatient 
from api.models.dicom_store_event import DicomStoreEvent 
# from api.models.dicom_study import DicomStudy 
# from api.models.dicom_series import DicomSeries 

api = Namespace('Application Entity', description='Dicom data related to the application entity')

# Application Entity 
@api.route('/application-entity', methods=['GET'])
class ApplicationEntityRoute(Resource):

    def get(self):
        return {'application_entities': ApplicationEntity.Schema(many=True).dump(ApplicationEntity.query.all())}

# # Dicom Store Event
# # belongs to an application entity
@api.route('/store-event', methods=['GET'])
class StoreEventRoute(Resource):

    def get(self):
        return {'store_event': DicomStoreEvent.Schema(many=True).dump(DicomStoreEvent.query.all())}

# # Dicom Patient
# # belongs to a store event
# @api.route('/patient', methods=['GET'])
# class DicomPatientRoute(Resource):

#     def get(self):
#         return {'dicom-patient': DicomPatient.Schema(many=True).dump(DicomPatient.query.all())}

# # Dicom Study
# # belongs to a patient
# @api.route('/study', methods=['GET'])
# class DicomStudyRoute(Resource):

#     def get(self):
#         return {'study': DicomStudy.Schema(many=True).dump(DicomStudy.query.all())}

# # Dicom series
# # belongs to a study
# @api.route('/series', methods=['GET'])
# class DicomSeriesRoute(Resource):

#     def get(self):
#         return {'series': DicomSeries.Schema(many=True).dump(DicomSeries.query.all())}
