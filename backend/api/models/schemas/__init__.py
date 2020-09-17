from marshmallow_sqlalchemy import ModelSchema
from api import db


class BaseSchema(ModelSchema):
    class Meta:
        ordered = True
        sqla_session = db.session


def add_schema(cls):
    class Schema(BaseSchema):
        class Meta(BaseSchema.Meta):
            model = cls

    cls.Schema = Schema
    return cls
