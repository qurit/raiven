from api.dicom import SCP


def test_scp_class() -> SCP:
    ae_title = "TEST_AE_TITLE"
    port = 11112

    scp = SCP(ae_title=ae_title, port=port)

    assert scp.ae_title == ae_title
    assert scp.port == port
    assert scp.get_ae().ae_title == scp.ae_title

    return scp


def test_scp_sever_startup_and_shutdown():
    scp = test_scp_class()

    scp.start_server()
    scp.shutdown()
