FROM python:3.8-slim
WORKDIR /src

RUN pip install pydicom numpy
COPY . .

ENV PICOM_INPUT_DIR /mnt/picom/input
ENV PICOM_OUTPUT_DIR /mnt/picom/ouput

CMD /bin/bash