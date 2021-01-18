# Containers
[Docker](https://docker.com/) Containers are the building blocks of Raiven's pipelines. Detailed below is the process of creating and uploading a container
so you can use it in a pipeline.

!!! tip "Language Support"
    RAIVEN supports any language so long as you can containerize your algorithm.

## Creating a Container
When creating a container, you should have a **Dockerfile** all the source code required to run your **algorithm**. In general,
all dockerfiles will need:

1. Install any dependencies you may require
2. Set the following environment variables:
    - `RAIVEN_INPUT_DIR=/mnt/raiven/input`
    - `RAIVEN_OUTPUT_DIR=/mnt/raiven/output`
3. Provide a command to execute your algorithm


### Dockerfile Example
Below is a sample dockerfile used when creating a container in python.
```dockerfile
FROM python:3.8-slim
WORKDIR /src

RUN pip install pydicom numpy
COPY . .

ENV RAIVEN_INPUT_DIR /mnt/raiven/input
ENV RAIVEN_OUTPUT_DIR /mnt/raiven/output

CMD python main.py
```

### Algorithm Example

An example algorithm that runs inside the container is shown below. In the code below, the algorithm reads all the dicom 
files from the input directory, doubles the value of their pixels, and then saves the new image to the output directory.

```python
import os

from pydicom import dcmread

INPUT_DIR = os.environ['PICOM_INPUT_DIR']
OUTPUT_DIR = os.environ['PICOM_OUTPUT_DIR']


if __name__ == '__main__':
    for root, dirs, files in os.walk(INPUT_DIR):
        for file in files:
            if file.endswith('.dcm'):
                ds = dcmread(os.path.join(root, file))

                pixels = ds.pixel_array
                pixels = pixels * 2
                ds.PixelData = pixels.tobytes()
                ds.save_as(os.path.join(OUTPUT_DIR, file))
```   
!!! note
    If you did not set up the input and output environment variables in the Dockerfile, you can set the 
    input and output directories to be `/mnt/raiven/input` and `/mnt/raiven/output`.


## Uploading a Container

1. Go to the _Containers_ :material-package-variant-closed: page
2. Fill out the "Add a Container" form
    * You must provide a container name and an attached file
3. Click **Add Container**

!!! warning
    Make sure to place both your dockerfile and source files in a zip file before uploading

## Editing a Container

1. Go to the _Containers_ :material-package-variant-closed: page
2. Click :material-pencil: next to the Container to be edited
    * Alternatively, click :material-delete: to completely delete the container
3. Edit the form
4. Click **Save Edits**
