from pydicom import dcmread

from pynetdicom import AE, StoragePresentationContexts
from pynetdicom.sop_class import CTImageStorage
import os

if __name__ == '__main__':
    ae = AE(ae_title='BC158VIPT1')
    ae.requested_contexts = StoragePresentationContexts

    assoc = ae.associate('localhost', 11112, ae_title='CT_QA')
    if assoc.is_established:
        print('ESTABLISHED')

        for root, _, files in os.walk('E:\\BCCRC\\dicom\\case1'):
            for file in files:
                if file.endswith('.dcm'):
                    ds = dcmread(os.path.join(root, file), force=True)
                    status = assoc.send_c_store(ds)
                    if not status:
                        print('Connection timed out, was aborted or received invalid response')
    else:
        print('Not established')

    assoc.release()