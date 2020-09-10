# PICOM
Build using python, flask, and nuxt, PICOM is full-featured application for building and maintaining DICOM image processing pipelines.

PICOM hope so fullfil these [user stories](./stories.md).

## Docker Deployment
```
docker stack deploy --compose-file swarm-compose.yml picom
docker stack rm picom
```