from pynetdicom import (
    AE, debug_logger, evt, AllStoragePresentationContexts,
    ALL_TRANSFER_SYNTAXES
)

debug_logger()

def handle_store(event):
    ds = event.dataset
    ds.file_meta = event.file_meta
    ds.save_as(ds.SOPInstanceUID, write_like_original=False)
    return 0x0000

def handle_echo(event):
    print("TESTING")
    return 0x0000
    

handlers = [(evt.EVT_C_STORE, handle_store), (evt.EVT_C_ECHO, handle_echo)]


ae = AE()
storage_sop_classes = [

ae = AE()
storage_sop_classes = [
     cx.abstract_syntax for cx in AllStoragePresentationContexts
]
for uid in storage_sop_classes:
    ae.add_supported_context(uid, ALL_TRANSFER_SYNTAXES)

ae.start_server(('', 11112), block=True, evt_handlers=handlers)