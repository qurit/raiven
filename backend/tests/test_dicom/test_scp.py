from api.dicom import SCP


def test_scp_class() -> SCP:
    ae_title = "TEST_AE_TITLE"
    port = 11112

    scp = SCP(ae_title=ae_title, port=port)

    assert scp.ae_title == ae_title
    assert scp.port == port
    assert scp.get_ae().ae_title == scp.ae_title

    return scp


def test_scp_sever_startup_and_shutdown():
    scp = test_scp_class()

    scp.start_server()
    scp.shutdown()


import os
from pydicom import dcmread, uid

if __name__ == '__main__':
    INPUT_DIR = 'C:\\Users\\Adam\\Programming\\picom\\uploads\\dicom_nodes\\30\\31\\3\\659'
    # INPUT_DIR = 'E:\\BCCRC\\dicom\\pyPET4RT'
    OUTPUT_DIR = 'C:\\Users\\Adam\\Programming\\picom\\test_out'


    for root, dirs, files in os.walk(INPUT_DIR):
        for file in files:
            if file.endswith('.dcm'):
                print('Reading', file)

                ds = dcmread(os.path.join(root, file), force=True)

                # print(ds)
                print(ds.file_meta)

                pixels = ds.pixel_array
                pixels = pixels * 2
                ds.PixelData = pixels.tobytes()
                ds.save_as(os.path.join(OUTPUT_DIR, file))
