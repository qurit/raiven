import os

from pynetdicom import (
    AE, debug_logger, evt, AllStoragePresentationContexts,
    ALL_TRANSFER_SYNTAXES
)
# from backend.api import db
# debug_logger()

def handle_store(event):
    """Handle EVT_C_STORE events."""
    print(event)
    print(event.assoc.requestor.address)
    print(event.assoc.requestor.port)
    print(str(event.assoc.requestor.ae_title, encoding='utf-8').strip())
    ds = event.dataset
    ds.file_meta = event.file_meta
    ds.save_as(ds.SOPInstanceUID, write_like_original=False)
    # print(ds)
    print("BLAHBLAHBLAH")
    print(ds.PatientID)
    # TMP_DIR = os.path.join(os.getcwd(), 'tmp')
    # path = os.path.join(TMP_DIR, ds.PatientId)
    # if not os.path.exists(path):
    #     os.mkdir(path)
    return 0x0000

handlers = [(evt.EVT_C_STORE, handle_store)]

ae = AE()
storage_sop_classes = [
     cx.abstract_syntax for cx in AllStoragePresentationContexts
]
for uid in storage_sop_classes:
    ae.add_supported_context(uid, ALL_TRANSFER_SYNTAXES)

ae.start_server(('', 11112), block=True, evt_handlers=handlers)