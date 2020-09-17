# PICOM
Build using python, flask, and nuxt, PICOM is full-featured application for building and maintaining DICOM image processing pipelines.

PICOM hopes to fulfill these [user stories](./stories.md).

## Development Using Docker
```
docker-compose up --build
```

Performing database migrations within a docker container.
```bash
# Init
docker exec picom_api_1 python manage.py manager init

# Migrate
docker exec picom_api_1 python manage.py manager migrate

# Upgrade
docker exec picom_api_1 python manage.py manager upgrade
```