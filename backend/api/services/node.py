from datetime import datetime

from api.models.dicom import DicomNode
from . import DatabaseService


class DicomNodeService(DatabaseService):

    def update_or_create_from_connection(self, title, host, **kwargs):
        if node := DicomNode.query(self._db).filter_by(title=title, host=host).first():
            node.last_connected = datetime.utcnow()
        else:
            DicomNode(
                **kwargs,
                title=title,
                host=host,
                first_connected=datetime.utcnow(),
                last_connected=datetime.utcnow()
            ).save(self._db)
