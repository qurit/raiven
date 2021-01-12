import os

from pydicom import dcmread
from pynetdicom import AE, StoragePresentationContexts
from pynetdicom.sop_class import VerificationSOPClass

from api.models.destination import Destination
from .assocation import Association, AssociationException


def send_dicom_folder(dest: Destination, abs_dicom_folder: str):
    """
    Send a dicom folder to a DICOM node using a c_store.
    """

    try:
        with Association(dest, StoragePresentationContexts) as assoc:
            for root, _, files in os.walk(abs_dicom_folder):
                for file in files:
                    if file.endswith('.dcm'):
                        ds = dcmread(os.path.join(root, file))
                        status = assoc.send_c_store(ds)
                        if not status:
                            print('Connection timed out, was aborted or received invalid response')

    except AssociationException as e:
        print(e)


def send_echo(dest: Destination):

    try:
        with Association(dest, VerificationSOPClass) as assoc:
            status = assoc.send_c_echo()
            return bool(status)

    except AssociationException:
        return False

