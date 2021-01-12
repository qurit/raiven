<p align="center">
  <img src="./assets/raiven-logo-text.svg" alt="Raiven Logo" style="height:300px"/>
</p>
<p align="center">
  <em>The Radiology Environment of the Future</em></br>
  <sub>Radiology + AI + Environment  = Raiven</sub>
</p>
<p align="center">
</p>

---

Build using python, fastapi, and nuxt, Raiven is full-featured application for building and maintaining DICOM image processing pipelines. Raiven hopes to become the radiology room of the future.


## Deployment

The easiest way to deploy Raiven is using docker. Raiven comes with a preconfigured compose file.

<div class="termy">

```console
$ docker-compose up -d
```
</div>

## Config

Configuration of Raiven can be done in multiple places. If you are using docker, configuration
can be done by modifying the `.env` file. Backend configuration can also be done by modifying `/backend/config.py` whilst
the frontend configuration can be done by modifying `/frontend/nuxt.config.js`. Configuration can also be done by
setting environment variables. The environment variables which can be set are found in `/backend/config.py`.

---

<p align="center">
  <em>Proudly Sponsored by <a href="https://qurit.ca">Qurit</a></em>
</p>
<p align="center">
  <img src="./assets/qurit-logo-text.png" alt="Qurit Logo" style="max-height: 100px" />
</p>
