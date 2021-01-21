from api import config
from api.models.user import User
from api.models.container import Container
from api.models.dicom import DicomNode


def populate_default_user(db):
    """ Adds a default internal user and default containers if they do not exist """

    if not (user := db.query(User).filter_by(username=config.INTERNAL_USERNAME).first()):
        user = User(username=config.INTERNAL_USERNAME, name=config.INTERNAL_USERNAME)
        user.save(db)

    if not db.query(Container).filter_by(user_id=user.id).all():
        [Container(user_id=user.id, is_shared=True, **kwargs).save(db) for kwargs in config.DEFAULT_CONTAINERS]

    if not db.query(DicomNode).filter_by(user_id=user.id).first():
        DicomNode(title='__RETURN__TO_SENDER__', host='*', output=True).save(db)
