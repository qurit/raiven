<p align="center">
  <img src="frontend/static/raiven-logo-text.svg" alt="Raiven Logo" height="300" />
</p>
<p align="center">
  <em>The Radiology Enviroment of the Future</em>
</p>
<p align="center">
<img alt="Docker API Image CI" src="https://github.com/qurit/raiven/workflows/Docker%20API%20Image%20CI/badge.svg?branch=master" />
<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/fastapi" />
<img alt="npm" src="https://img.shields.io/npm/v/npm" />

</p>

---
Build using python, flask, and nuxt, Raiven is full-featured application for building and maintaining DICOM image processing pipelines.  Raiven hopes to become the radiology room of the future.

Raiven hopes to fulfill these [user stories](./stories.md).

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
---
<p align="center">
  <em>Proudly Created by <a href="https://qurit.ca">Quirt</a></em>
</p>
<p align="center">
  <img src="frontend/static/qurit-logo-text.png" alt="Qurit Logo" height="75" />
</p>
