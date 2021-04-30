# Backend

The backend is built primarily using [FastAPI](https://fastapi.tiangolo.com/) in Python, with a [PostgreSQL](https://www.postgresql.org/) database.

## Models

The models define the entity-relationship model in the database, and can be found under `\backend\api\models`.

## Schemas

The definitions of how data is to be sent and received by the internal API. They can be found under `\backend\api\schemas`.

## Routes

The internal API routes that can be used by the frontend, and pull information from the database. They can be found under `\backend\api\routes`. Middleware for the routes can be found under `\backend\api\middleware`.

## Pipelining Logic

Basically magic by Adam.
