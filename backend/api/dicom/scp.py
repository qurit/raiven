import os
import uuid
import datetime
import pathlib
import shutil

from pynetdicom import AE, evt, debug_logger
from pydicom.filewriter import write_file_meta_info
from pynetdicom.presentation import AllStoragePresentationContexts
from pynetdicom.sop_class import VerificationSOPClass
from pydicom import uid

from api import config
from api.database import worker_session as session
from api.models.dicom import DicomNode, DicomPatient, DicomStudy, DicomSeries
from api.pipelining import DicomIngestController

# debug_logger()

# Use a hash map
CONNECTIONS = {}

REJECTED_PERMANENT = 0x01
REJECTED_TRANSIENT = 0x02
SOURCE_SERVICE_USER = 0x01
SOURCE_PROVIDER_USER = 0x03
DIAG_CALLING_AET_NOT_RECOGNIZED = 0x03
DIAG_CALLED_AET_NOT_RECOGNIZED = 0x07
DIAG_LOCAL_LIMIT_EXCEEDED = 0x02


def encode_aet(ae_title_bytes: bytes) -> str:
    return str(ae_title_bytes, encoding='utf-8').strip()


def get_ae_titles(event):
    return (
        encode_aet(event.assoc.requestor.primitive.calling_ae_title),
        encode_aet(event.assoc.requestor.primitive.called_ae_title)
    )


def handle_association_request(event):
    requestor_ae_title, called_ae_title = get_ae_titles(event)

    # TODO: Not in list of allowed connections and allow push to pipe
    if config.SCP_AE_TITLE not in called_ae_title:
        event.assoc.acse.send_reject(REJECTED_PERMANENT, SOURCE_SERVICE_USER, DIAG_CALLED_AET_NOT_RECOGNIZED)

    # ALREADY CONNECTED
    elif requestor_ae_title in CONNECTIONS:
        event.assoc.acse.send_reject(REJECTED_TRANSIENT, SOURCE_PROVIDER_USER, DIAG_LOCAL_LIMIT_EXCEEDED)
    else:
        path = pathlib.Path(config.UPLOAD_DIR) / 'tmp' / str(uuid.uuid1())
        CONNECTIONS[requestor_ae_title] = path
        path.mkdir(parents=True)


def handle_association_release(event):
    """ Upon release start a task for all the received files to be ingested into the db """

    requestor_ae_title, called_ae_title = get_ae_titles(event)
    calling_host, calling_port = event.assoc.requestor.address, event.assoc.requestor.port

    if requestor_ae_title in CONNECTIONS:


        # Start task
        DicomIngestController.ingest_folder(
            folder=CONNECTIONS[requestor_ae_title],
            calling_aet=requestor_ae_title,
            calling_host=calling_host,
            calling_port=calling_port,
            called_aet=called_ae_title
        )

        del CONNECTIONS[requestor_ae_title]

    return 0x0000


def handle_store(event):
    """ Handles EVT_C_STORE """
    requestor_ae_title, called_ae_title = get_ae_titles(event)

    path = CONNECTIONS[requestor_ae_title] / (event.request.AffectedSOPInstanceUID + '.dcm')
    with open(path, 'wb') as f:
        f.write(b'\x00' * 128)
        f.write(b'DICM')
        # TODO: check this is still needed
        # event.file_meta.TransferSyntaxUID = uid.ImplicitVRLittleEndian
        write_file_meta_info(f, event.file_meta)
        f.write(event.request.DataSet.getvalue())

    return 0x0000


class SCP:
    _handlers = [
        (evt.EVT_REQUESTED, handle_association_request),
        (evt.EVT_RELEASED, handle_association_release),
        (evt.EVT_C_STORE, handle_store),
    ]

    def __init__(self, ae_title='PICOM_SCP', host='localhost', port=11112, debug=False):
        self.ae_title = ae_title
        self.host = host
        self.port = port

        self._ae = AE(ae_title)
        self._ae.supported_contexts = AllStoragePresentationContexts
        self._ae.add_supported_context(VerificationSOPClass)

        if debug:
            debug_logger()

    def start_server(self, blocking=False):
        self._ae.start_server((self.host, self.port), block=blocking, evt_handlers=self._handlers)

    def stop_server(self):
        self._ae.shutdown()

    def get_ae(self) -> AE:
        return self._ae


if __name__ == '__main__':
    print("Starting server...")
    print("Waiting for connections...")
    scp = SCP()
    scp.start_server(blocking=False)
    scp.stop_server()
