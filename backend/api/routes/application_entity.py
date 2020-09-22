from typing import List
from pydantic import BaseModel

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from api import session, models, schemas
router = APIRouter()


@router.get("/ae/", response_model=List[schemas.ApplicationEntity])
def get_application_entities(db: Session = Depends(session)):
    return db.query(models.dicom.ApplicationEntity).all()


@router.post("/ae/", response_model=schemas.ApplicationEntity)
def create_application_entity(ae: schemas.ApplicationEntityCreate, db: Session = Depends(session)):
    return models.dicom.ApplicationEntity(title=ae.title).save(db)


#
# @router.post("/ae/", response_model=schemas.ApplicationEntity)
# def add_application_entity(application_entity: schemas.ApplicationEntityCreate):
#     print(type(application_entity))
#     print(application_entity)
#     db_ae = models.dicom.ApplicationEntity(**application_entity.dict()).save(db)
#
#     return db_ae

#
# # Application Entity
# @api.route('/application-entity', methods=['GET', 'POST', 'DELETE'])
# class ApplicationEntityRoute(Resource):
#     def get(self):
#         return {'application_entities': ApplicationEntity.Schema(many=True).dump(ApplicationEntity.query.all())}
#
#     def delete(self):
#         data = request.get_json()
#         ApplicationEntity.query.filter(ApplicationEntity.id == data.get('id')).delete()
#         db.session.commit()
#         return "Application Entity deleted"
#
#     @api.expect(application_entity_model)
#     def post(self):
#         data = request.get_json()
#         newApplicationEntity = ApplicationEntity(title=data.get('title'))
#         db.session.add(newApplicationEntity)
#         db.session.commit()
#         return "Application Entity added"
#
# @api.route('/application-entity/<id>', methods=['GET', 'PUT', 'DELETE'])
# class ApplicationEntityRoute(Resource):
#     def get(self, id):
#         return {'application-entity': ApplicationEntity.Schema(many=False).dump(ApplicationEntity.query.filter(ApplicationEntity.id == id).first())}
#
#     def put(self, id):
#         data = request.get_json()
#         newApplicationEntity = ApplicationEntity.query.filter(ApplicationEntity.id == id).first()
#         newApplicationEntity.title = data.get('title')
#         db.session.commit()
#         return "Application Entity updated"
#
#     def delete(self, id):
#         ApplicationEntity.query.filter(ApplicationEntity.id == id).delete()
#         db.session.commit()
#         return "Application Entity deleted"
#
# # # Dicom Store Event
# # # belongs to an application entity
# @api.route('/store-event', methods=['GET'])
# class StoreEventRoute(Resource):
#
#     def get(self):
#         return {'store_event': DicomStoreEvent.Schema(many=True).dump(DicomStoreEvent.query.all())}
#
# # # Dicom Patient
# # # belongs to a store event
# @api.route('/patient', methods=['GET'])
# class DicomPatientRoute(Resource):
#
#     def get(self):
#         return {'dicom-patient': DicomPatient.Schema(many=True).dump(DicomPatient.query.all())}
#
# # # Dicom Study
# # # belongs to a patient
# @api.route('/study', methods=['GET'])
# class DicomStudyRoute(Resource):
#
#     def get(self):
#         return {'study': DicomStudy.Schema(many=True).dump(DicomStudy.query.all())}
#
# # # Dicom series
# # # belongs to a study
# @api.route('/series', methods=['GET'])
# class DicomSeriesRoute(Resource):
#
#     def get(self):
#         return {'series': DicomSeries.Schema(many=True).dump(DicomSeries.query.all())}
