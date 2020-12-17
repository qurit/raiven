import os

from pydicom import dcmread
from pynetdicom import AE, StoragePresentationContexts
from pynetdicom.sop_class import CTImageStorage


# Replace with your own path to a test folder
UPLOAD_DIR = 'E:\\BCCRC\\dicom\\pyPET4RT'

if __name__ == '__main__':
    """ Small test program that uploads an entire dicom directory to a node """

    ae = AE(ae_title='BC158VIPT1')
    ae.requested_contexts = StoragePresentationContexts

    assoc = ae.associate('localhost', 11112, ae_title='RAIVEN')
    if assoc.is_established:
        print('ESTABLISHED')

        for root, _, files in os.walk(UPLOAD_DIR):
            for file in files:
                if file.endswith('.dcm'):
                    ds = dcmread(os.path.join(root, file))
                    status = assoc.send_c_store(ds)
                    if not status:
                        print('Connection timed out, was aborted or received invalid response')
    else:
        print('Not established')

    assoc.release()
