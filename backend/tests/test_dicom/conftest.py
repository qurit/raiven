import pytest
from pynetdicom import AE, StoragePresentationContexts
from pynetdicom.sop_class import VerificationSOPClass

from api.dicom.scp import SCP
from tests import config


@pytest.fixture(scope="module", autouse="True")
def scp_server():
    scp_server = SCP(ae_title=config.SCP_AE_TITLE, host=config.SCP_HOST, port=config.SCP_PORT)
    scp_server.start_server(blocking=False)

    yield

    scp_server.stop_server()


@pytest.fixture
def association():
    ae = AE(ae_title='Test AE')
    ae.requested_contexts = StoragePresentationContexts[:-1]
    ae.add_requested_context(VerificationSOPClass)

    assoc = ae.associate(config.SCP_HOST, config.SCP_PORT, ae_title=config.SCP_AE_TITLE)
    assert assoc.is_established

    yield assoc

    assoc.release()


