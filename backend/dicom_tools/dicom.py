from pydicom.dataset import Dataset
import pydicom
from pynetdicom import AE, evt, build_role, debug_logger
# import pandas as pd

# debug_logger()


def c_echo():
    from pynetdicom.sop_class import VerificationSOPClass
    assoc = get_assoc(VerificationSOPClass)

    status = assoc.send_c_echo()
    if status:
        # If the verification request succeeded this will be 0x0000
        print('[GOOD]: C-ECHO request status: '.format(status.Status))
    else:
        print('[ERROR]: C-ECHO Connection timed out, was aborted or received invalid response')
    assoc.release()


def c_find():
    from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind as ModelFind

    assoc = get_assoc(ModelFind)

    ds = Dataset()
    ds.StudyInstanceUID = '1.2.840.113619.2.290.3.84544369.339.1344001433.892'
    ds.SeriesInstanceUID = '1.2.840.113619.2.290.3.84544369.339.1344001433.896.3'
    ds.PatientID = '1210677'
    ds.PPSStartDate = ''
    ds.SeriesDate = ''
    ds.StudyDate = ''
    # ds.ModalitiesInStudy = 'CT'

    ds.QueryRetrieveLevel = 'SERIES'

    responses = assoc.send_c_find(ds, ModelFind)
    for (status, dataset) in responses:
        if status and dataset is not None:
            # print(type(dataset))
            print(dataset)
            # print(dataset.ModalitiesInStudy)
            print('-------')
            # print('[GOOD]: C-FIND query status: 0x{0:04X}'.format(status.Status))
        elif not status:
            print('[ERROR]: C-FIND connection timed out, was aborted or received invalid response')

    # Release the association
    assoc.release()


def c_get():
    from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelGet as ModelGet, CTImageStorage

    def handle_store(event):
        """Handle a C-STORE request event."""
        ds = event.dataset
        ds.file_meta = event.file_meta
        ds.save_as('test.dcm', write_like_original=False)
        return 0x0000

    handlers = [(evt.EVT_C_STORE, handle_store)]
    role = build_role(CTImageStorage, scp_role=True)
    assoc = get_assoc([ModelGet, CTImageStorage], ext_neg=[role], evt_handlers=handlers)

    ds = Dataset()
    ds.StudyInstanceUID = ''
    ds.PatientID = '1210677'
    ds.ModalitiesInStudy = 'CT'
    ds.QueryRetrieveLevel = 'STUDY'

    responses = assoc.send_c_get(ds, ModelGet)
    for (status, identifier) in responses:
        if status:
            print('[GOOD]: C-GET query status: 0x{0:04X}'.format(status.Status))
        else:
            print('[ERROR]: C-GET connection timed out, was aborted or received invalid response')

    # Release the association
    assoc.release()

# Error: Data Set does not match SOP Class A900


def c_move():
    from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelMove as ModelMove

    ds = Dataset()
    ds.StudyInstanceUID = '1.2.840.113619.2.290.3.84544369.339.1344001433.892'
    ds.SeriesInstanceUID = '1.2.840.113619.2.290.3.84544369.339.1344001433.896.3'
    ds.PatientID = '1210677'
    ds.SeriesDate = ''
    # ds.ModalitiesInStudy = 'CT'
    ds.SeriesDescription = ''
    ds.QueryRetrieveLevel = 'SERIES'

    # Associate with peer AE at IP 127.0.0.1 and port 11112
    assoc = get_assoc(ModelMove)

    if assoc.is_established:
        # Use the C-MOVE service to send the identifier
        responses = assoc.send_c_move(ds, b'CTP', ModelMove)
        for (status, identifier) in responses:
            if status:
                print('[GOOD]: C-MOVE query status: 0x{0:04x}'.format(status.Status))
            else:
                print('[ERROR]: C-MOVE Connection timed out, was aborted or received invalid response')

        # Release the association
        assoc.release()
    else:
        print('Association rejected, aborted or never connected')


def c_store():
    from pynetdicom.sop_class import CTImageStorage, RawDataStorage
    from pydicom import dcmread


    ds = dcmread('test.img')

    assoc = get_assoc([CTImageStorage, '1.2.840.113619.4.30'])
    if assoc.is_established:

        status = assoc.send_c_store(ds)

        # Check the status of the storage request
        if status:
            # If the storage request succeeded this will be 0x0000
            print('C-STORE request status: 0x{0:04x}'.format(status.Status))
        else:
            print('Connection timed out, was aborted or received invalid response')

        # Release the association
        assoc.release()
    else:
        print('Association rejected, aborted or never connected')


def get_assoc(context, **kwargs):
    ae = AE()
    # ae = AE()
    [ae.add_requested_context(c) for c in context] if type(context) is list else ae.add_requested_context(context)

    # assoc = ae.associate('10.9.2.246', 11124, ae_title='LYMPH_BCCAN', **kwargs)
    # assoc = ae.associate('mit.bccrc.ca', 4242, ae_title='ORTHANC', **kwargs)
    assoc = ae.associate('10.1.55.30', 107, ae_title='STENTOR_QRP', **kwargs)
    assert assoc.is_established, 'Association rejected, aborted or never connected with {}'.format(context)
    return assoc


if __name__ == "__main__":
    debug_logger()
    # c_echo()
    # c_find()
    # # c_get()
    # c_move()
    # # c_store()