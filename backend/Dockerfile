FROM python:3.8-slim
WORKDIR /backend

# Install app reqs and copy src
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1

COPY . .

EXPOSE 5000
CMD python asgi.py
