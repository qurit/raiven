from pydicom.dataset import Dataset
import pydicom
from pynetdicom import AE, evt, build_role, debug_logger

# debug_logger()


def c_echo():
    from pynetdicom.sop_class import VerificationSOPClass
    assoc = get_assoc(VerificationSOPClass)

    status = assoc.send_c_echo()
    if status:
        # If the verification request succeeded this will be 0x0000
        print('[GOOD]: C-ECHO request status: 0x{0:04x}'.format(status.Status))
    else:
        print('[ERROR]: C-ECHO Connection timed out, was aborted or received invalid response')
    assoc.release()


def c_find():
    from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind as ModelFind

    assoc = get_assoc(ModelFind)

    dataset = Dataset()
    dataset.PatientName = '*'
    dataset.PatientID = '11788759296811'
    dataset.PatientSex = ''
    # dataset.PatientBirthDate = ''
    dataset.StudyDescription = ''
    dataset.SeriesInstanceUID = ''
    dataset.QueryRetrieveLevel = "SERIES"

    responses = assoc.send_c_find(dataset, ModelFind)
    for (status, identifier) in responses:
        if status and identifier:
            print(identifier)
            print('[GOOD]: C-FIND query status: 0x{0:04X}'.format(status.Status))
        elif not status:
            print('[ERROR]: C-FIND connection timed out, was aborted or received invalid response')

    # Release the association
    assoc.release()


def c_get():
    from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelGet as ModelGet, MRImageStorage

    def handle_store(event):
        """Handle a C-STORE request event."""
        ds = event.dataset
        ds.file_meta = event.file_meta

        # Save the dataset using the SOP Instance UID as the filename
        ds.save_as('test.dcm', write_like_original=False)

        # Return a 'Success' status
        return 0x0000

    handlers = [(evt.EVT_C_STORE, handle_store)]
    role = build_role(MRImageStorage, scp_role=True)
    assoc = get_assoc([ModelGet, MRImageStorage], ext_neg=[role], evt_handlers=handlers)

    ds = Dataset()
    ds.QueryRetrieveLevel = 'SERIES'
    # ds.PatientID = '11788759296811'
    # ds.StudyInstanceUID = '1.2.276.0.50.192168001099.7810872.14547392.270'
    ds.SeriesInstanceUID = '1.2.276.0.50.192168001099.7810872.14547392.458'

    responses = assoc.send_c_get(ds, ModelGetPPP)
    for (status, identifier) in responses:
        if status:
            print('[GOOD]: C-GET query status: 0x{0:04X}'.format(status.Status))
        else:
            print('[ERROR]: C-GET connection timed out, was aborted or received invalid response')

    # Release the association
    assoc.release()


def c_move():
    from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelMove as ModelMove
    ds = Dataset()
    ds.QueryRetrieveLevel = 'SERIES'
    ds.PatientID = '11788759296811'
    ds.StudyInstanceUID = '1.2.276.0.50.192168001099.7810872.14547392.270'
    ds.SeriesInstanceUID = '1.2.276.0.50.192168001099.7810872.14547392.458'

    # Associate with peer AE at IP 127.0.0.1 and port 11112
    assoc = get_assoc(ModelMove)

    if assoc.is_established:
        # Use the C-MOVE service to send the identifier
        responses = assoc.send_c_move(ds, b'PYNETDICOM', ModelMove)
        for (status, identifier) in responses:
            if status:
                print('[GOOD]: C-MOVE query status: 0x{0:04x}'.format(status.Status))
            else:
                print('[ERROR]: C-MOVE Connection timed out, was aborted or received invalid response')

        # Release the association
        assoc.release()
    else:
        print('Association rejected, aborted or never connected')


def get_assoc(context, **kwargs):
    ae = AE('PICOM')
    [ae.add_requested_context(c) for c in context] if type(context) is list else ae.add_requested_context(context)

    # assoc = ae.associate('localhost', 4243, ae_title='ORTHANC', **kwargs)
    assoc = ae.associate('localhost', 11112, ae_title='MY_SCP', **kwargs)
    assert assoc.is_established, 'Association rejected, aborted or never connected with {}'.format(context)
    return assoc


if __name__ == "__main__":
    # c_echo()
    # c_find()
    from pydicom.uid import ExplicitVRLittleEndian

    from pynetdicom import AE, debug_logger, evt
    from pynetdicom.sop_class import CTImageStorage, VerificationSOPClass

    debug_logger()


    def handle_store(event):
        """Handle EVT_C_STORE events."""
        ds = event.dataset
        ds.file_meta = event.file_meta

        # Save the dataset using the SOP Instance UID as the filename
        ds.save_as('test.dcm', write_like_original=False)

        # Return a 'Success' status
        return 0x0000


    handlers = [(evt.EVT_C_STORE, handle_store)]

    ae = AE('MY_SCP')
    ae.add_supported_context(VerificationSOPClass, ExplicitVRLittleEndian)
    ae.add_supported_context(CTImageStorage, ExplicitVRLittleEndian)
    ae.start_server(('localhost', 11112), block=False, evt_handlers=handlers)
    c_echo()