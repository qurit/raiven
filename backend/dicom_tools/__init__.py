# from pydicom.dataset import Dataset
# import pydicom
# from pynetdicom import AE, evt, build_role, debug_logger
# from . import utils, echo

# if __name__ == "__main__":
#     # c_echo()
#     # c_find()
#     from pydicom.uid import ExplicitVRLittleEndian
#
#     from pynetdicom import AE, debug_logger, evt
#     from pynetdicom.sop_class import CTImageStorage, VerificationSOPClass
#
#     debug_logger()
#
#
#     def handle_store(event):
#         """Handle EVT_C_STORE events."""
#         ds = event.dataset
#         ds.file_meta = event.file_meta
#
#         # Save the dataset using the SOP Instance UID as the filename
#         ds.save_as('test.dcm', write_like_original=False)
#
#         # Return a 'Success' status
#         return 0x0000
#
#
#     handlers = [(evt.EVT_C_STORE, handle_store)]
#
#     ae = AE('MY_SCP')
#     ae.add_supported_context(VerificationSOPClass, ExplicitVRLittleEndian)
#     ae.add_supported_context(CTImageStorage, ExplicitVRLittleEndian)
#     ae.start_server(('localhost', 11112), block=False, evt_handlers=handlers)
#     c_echo()