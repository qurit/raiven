import os

from pydicom import dcmread
from pynetdicom import AE
from pynetdicom.sop_class import VerificationSOPClass

from api.dicom import SCP

from tests import config, models


def test_scp_class(ae_title: str = "TEST_AE_TITLE", port: int = 11010) -> SCP:
    scp = SCP(ae_title=ae_title, port=port)

    assert scp.ae_title == ae_title
    assert scp.port == port

    return scp


def test_scp_sever_startup_and_shutdown():
    scp = test_scp_class()

    scp.start_server()
    scp.stop_server()


def test_scp_association():
    ae = AE(ae_title='Test AE')
    ae.add_requested_context(VerificationSOPClass)

    assoc = ae.associate(config.SCP_HOST, config.SCP_PORT, ae_title=config.SCP_AE_TITLE)
    assert assoc.is_established

    assoc.release()


def test_scp_association_rejected():
    ae = AE(ae_title='Test AE')
    ae.add_requested_context(VerificationSOPClass)

    assoc = ae.associate(config.SCP_HOST, config.SCP_PORT, ae_title='randomAET')
    assert not assoc.is_established

    assoc.release()


def test_same_ae_connect():
    ae = AE(ae_title='Test Multiple')
    ae.add_requested_context(VerificationSOPClass)

    assoc = ae.associate(config.SCP_HOST, config.SCP_PORT, ae_title=config.SCP_AE_TITLE)
    assert assoc.is_established

    assoc_fail = ae.associate(config.SCP_HOST, config.SCP_PORT, ae_title=config.SCP_AE_TITLE)
    assert not assoc_fail.is_established

    assoc.release()
    assoc_fail.release()


# def test_scp_pipeline_association():
#     ae = AE(ae_title='Test AE')
#     ae.add_requested_context(VerificationSOPClass)
#
#     assoc = ae.associate(config.SCP_HOST, config.SCP_PORT, ae_title='RVP-my-pipe')
#     assert assoc.is_established
#     assert False


def test_echo(association):
    status = association.send_c_echo()
    assert status


def test_store(db, association):
    assert os.path.exists(mock_path := os.path.join(os.path.dirname(__file__), 'mock_data'))

    for root, _, files in os.walk(mock_path):
        for file in files:
            if file.endswith('.dcm'):
                ds = dcmread(os.path.join(root, file))
                uid = ds.SeriesInstanceUID

                if series := models.dicom.DicomSeries.query(db).filter_by(series_instance_uid=uid).all():
                    [s.delete(db) for s in series]
                    db.commit()

                status = association.send_c_store(ds)
                assert status
                # assert models.dicom.DicomSeries.query(db).filter_by(series_instance_uid=uid).first()
#
#
# # noinspection DuplicatedCode
# def test_store_same_instance(db, association):
#     assert os.path.exists(mock_path := os.path.join(os.path.dirname(__file__), 'mock_data'))
#
#     uid_list = []
#     for root, _, files in os.walk(mock_path):
#         for file in files:
#             if file.endswith('.dcm'):
#                 ds = dcmread(os.path.join(root, file))
#                 uid = ds.SeriesInstanceUID
#                 uid_list.append(uid)
#
#                 if series := models.dicom.DicomSeries.query(db).filter_by(series_instance_uid=uid).all():
#                     [s.delete(db) for s in series]
#                     db.commit()
#
#                 status = association.send_c_store(ds)
#                 assert status
#
#                 status = association.send_c_store(ds)
#                 assert status
#
#     for uid in uid_list:
#         # TODO: Should we be able to the same image twice?
#         assert len(models.dicom.DicomSeries.query(db).filter_by(series_instance_uid=uid).all()) == 1
#
#
