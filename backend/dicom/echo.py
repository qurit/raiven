from pynetdicom.sop_class import VerificationSOPClass

from dicom.utils import Modality


def echo(modality: Modality):

    with modality as assoc:
        assoc.send_c_echo()

        if status:
            # If the verification request succeeded this will be 0x0000
            print('[GOOD]: C-ECHO request status: 0x{0:04x}'.format(status.Status))
        else:
            print('[ERROR]: C-ECHO Connection timed out, was aborted or received invalid response')
