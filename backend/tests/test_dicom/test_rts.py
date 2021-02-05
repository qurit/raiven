import os
from time import sleep

from pydicom import dcmread
from pynetdicom import AE, evt, AllStoragePresentationContexts, StoragePresentationContexts

from api.queries.internal import get_return_to_sender
from api.schemas.dicom import DicomNode as DicomNodeSchema

from tests import client, config
from tests.test_models.test_containers import create_and_test_container
from tests.test_models.test_pipelines import LinearPipelineFactory
from tests.test_pipelining.test_build import build_container_foreground
from tests.test_dicom.test_scp import perform_store, join

PORT = 11114


def custom_store_scp(ae_title, storage_folder):

    def handle_store(event):
        ds = event.dataset
        ds.file_meta = event.file_meta
        ds.save_as(str(storage_folder / ds.SOPInstanceUID), write_like_original=False)
        return 0x0000

    handlers = [(evt.EVT_C_STORE, handle_store)]

    ae = AE(ae_title=ae_title)
    ae.supported_contexts = AllStoragePresentationContexts

    return ae, handlers


def custom_store_scu(ae_title):
    ae = AE(ae_title=ae_title)
    ae.requested_contexts = StoragePresentationContexts

    return ae


# TODO: this test only works like once a minute
def test_return_to_sender(db, stub_broker, stub_worker, authorization_header, tmp_folder):
    assert os.path.exists(mock_path := os.path.join(os.path.dirname(__file__), 'mock_data'))
    assert os.path.exists(file_path := os.path.join(mock_path, 'simple_container.zip'))
    assert os.path.isfile(file_path)

    factory = LinearPipelineFactory(db, 'rts_pipeline', ae_title='RTS')
    rts_container = DicomNodeSchema.from_orm(get_return_to_sender(db))
    factory.add_output_container(rts_container)
    pipeline = factory.create_pipeline(client, authorization_header)

    pipeline_aet = config.PIPELINE_AE_PREFIX + pipeline['ae_title']

    # Sending images
    ae = custom_store_scu('RTS')
    assoc = ae.associate(config.SCP_HOST, config.SCP_PORT, ae_title=pipeline_aet, bind_address=('', PORT))
    assert assoc.is_established
    perform_store(assoc, mock_path)
    assoc.release()

    # Starting the RTS server
    scp, handlers = custom_store_scp('RTS', storage_folder=tmp_folder)
    scp.start_server(('', PORT), evt_handlers=handlers, block=False)

    # Ensure detached SCP server has enough time to send job to worker before .join
    sleep(2)
    join(stub_broker, stub_worker)
    scp.shutdown()

    # Making sure files are the same
    received_files = [str(f.stem) for f in tmp_folder.iterdir()]
    for f in os.listdir(mock_path):
        if f.endswith('.dcm'):
            ds = dcmread(os.path.join(mock_path, f))

            # TODO: COMPARE FILES
            # # assert ds.SOPInstanceUID in received_files
            # received_ds = dcmread(str(tmp_folder / ds.SOPInstanceUID))
            #
            # # assert ds.SOPInstanceUID == received_ds.SOPInstanceUID
            # assert ds.pixel_array == received_ds.pixel_array
