from typing import Union, List

from pynetdicom import AE, AllStoragePresentationContexts

from api import config
from api.models.dicom import DicomNode


class AssociationException(Exception):
    def __init__(self, ae_title):
        super().__init__(f'Association with {ae_title} could not be made.')


class Association:
    __association = None

    def __init__(self, scp: DicomNode, contexts: Union[str, List[str]] = AllStoragePresentationContexts, **kwargs):
        self.host = scp.host
        self.port = scp.port
        self.ae_title = scp.title
        self.contexts = contexts
        self.kwargs = kwargs

    def __enter__(self):
        self.__association = self.__get_assoc()
        return self.__association

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__association.release()
        self.__association = None

    def __get_assoc(self):
        ae = AE(ae_title=config.SCP_AE_TITLE)

        if type(self.contexts) is list:
            ae.requested_contexts = self.contexts
        else:
            ae.add_requested_context(self.contexts)

        assoc = ae.associate(addr=self.host, port=self.port, ae_title=self.ae_title, **self.kwargs)

        if not assoc.is_established:
            raise AssociationException(ae_title=self.ae_title)

        return assoc
