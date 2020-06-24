FROM python:3.8-slim
WORKDIR /backend

RUN pip install gunicorn

# Install app reqs and copy src
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 5000
CMD gunicorn --bind 0.0.0.0:5000 wsgi
