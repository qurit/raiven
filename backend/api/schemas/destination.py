from . import BaseModel, BaseORMModel


class Destination(BaseORMModel):
    host: str
    port: int
    full_name: str


class CreateDestination(BaseModel):
    host: str
    port: int


class UserDestination(BaseORMModel):
    destination: Destination
