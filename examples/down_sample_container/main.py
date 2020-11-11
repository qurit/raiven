import os

from pydicom import dcmread

INPUT_DIR = os.environ['PICOM_INPUT_DIR']
OUTPUT_DIR = os.environ['PICOM_OUTPUT_DIR']


"""
A example Raiven container that down samples an image by a factor of 8.
https://pydicom.github.io/pydicom/stable/auto_examples/image_processing/plot_downsize_image.html
"""

if __name__ == '__main__':
    for root, dirs, files in os.walk(INPUT_DIR):
        for file in files:
            if file.endswith('.dcm'):
                ds = dcmread(os.path.join(root, file))

                data = ds.pixel_array
                ds.PixelData = data[::8, ::8].tobytes()
                ds.Rows, ds.Columns = data_downsampling.shape

                ds.save_as(os.path.join(OUTPUT_DIR, file))
