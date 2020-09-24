import os

from pydicom import dcmread

INPUT_DIR = os.environ['PICOM_INPUT_DIR']
OUTPUT_DIR = os.environ['PICOM_OUTPUT_DIR']


if __name__ == '__main__':

    for file in os.listdir(INPUT_DIR):
        if file.endswith('.dcm'):

            ds = dcmread(os.path.join(INPUT_DIR, file))
            pixels = ds.pixel_array
            pixels = pixels * 2
            ds.PixelData = pixels.tobytes()
            ds.save_as(os.path.join(OUTPUT_DIR, file))

