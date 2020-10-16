from . import BaseModel, BaseORMModel


class Destination(BaseORMModel):
    host: str
    port: int
    full_name: str
