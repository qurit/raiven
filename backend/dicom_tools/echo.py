from pynetdicom.sop_class import VerificationSOPClass
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind as ModelFind
from pydicom.dataset import Dataset
from pynetdicom import debug_logger

from dicom_tools.utils import Modality, Association


def echo(modality: Modality):
    print(modality)

    with Association(modality, VerificationSOPClass) as assoc:
        status = assoc.send_c_echo()

        if status:
            # If the verification request succeeded this will be 0x0000
            print(status)
            print('[GOOD]: C-ECHO request status: 0x{0:04x}'.format(status.Status))
        else:
            print('[ERROR]: C-ECHO Connection timed out, was aborted or received invalid response')


def execute_query(modality: Modality, query: Dataset) -> list:
    results = []

    with Association(modality, ModelFind) as assoc:
        for (status, ds) in assoc.send_c_find(query, ModelFind):
            if status and ds is not None:
                results.append(ds)

    return results


if __name__ == '__main__':
    # debug_logger()

    m = Modality('127.0.0.1', 4242, 'ORTHANC')
    echo(m)


