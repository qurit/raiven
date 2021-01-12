import pytest
from pynetdicom import AE, StoragePresentationContexts, debug_logger
from pynetdicom.sop_class import VerificationSOPClass

from api.dicom.scp import SCP
from tests import config


@pytest.fixture(scope="module", autouse="True")
def scp_server():
    scp_server = SCP(ae_title=config.SCP_AE_TITLE, host=config.SCP_HOST, port=config.SCP_PORT)
    scp_server.start_server(blocking=False)

    yield

    scp_server.stop_server()
