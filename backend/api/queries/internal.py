from typing import List

from api import config
from api.models.user import User
from api.models.container import Container
from api.models.dicom import DicomNode


def get_internal_user(db) -> User:
    return db.query(User).filter_by(username=config.INTERNAL_USERNAME).first()


def get_default_containers(db) -> List[Container]:
    user = get_internal_user(db)

    return db.query(Container).filter_by(user_id=user.id).all()


def get_return_to_sender(db) -> DicomNode:
    user = get_internal_user(db)

    return db.query(DicomNode).filter_by(user_id=user.id).first()
