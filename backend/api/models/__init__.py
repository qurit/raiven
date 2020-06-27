from bson import ObjectId
from flask_restx import fields, Model

from api import db


class BaseModel:
    def __init__(self, **kwargs):
        [self.__setattr__(k, v) for k, v in kwargs.items()]

    @property
    def in_db(self):
        return hasattr(self, '_id') and self._id

    @classmethod
    def model(cls, name='Base'):
        return Model(name, {'_id': fields.String})

    @classmethod
    def list_model(cls):
        m = cls.model()
        return Model(f'{m.name} list', {f'{m.name}s': fields.List(fields.Nested(m))})


def collection(cls: BaseModel) -> BaseModel:
    """
    Decorator which add mongo db utility functions to model
    :param cls: class to make awesome
    :return: super charged class
    """

    def insert(obj):
        assert not obj.in_db, 'OBJECT IS ALREADY IN DB'
        _id = obj.__collection__.insert_one(vars(obj)).inserted_id
        setattr(obj, '_id', _id)
        return obj

    def update(obj):
        assert obj.in_db, 'OBJECT IS NOT IN DB'
        obj.__collection__.replace_one({'_id': obj._id}, vars(obj))

    setattr(cls, '__collection__', db[f'{cls.__name__.lower()}s'])
    setattr(cls, 'insert', insert)
    setattr(cls, 'update', update)

    return cls


@collection
class User(BaseModel):

    def __init__(self, username: str = None, name=None, title=None, department=None, company=None, last_seen=None, **kwargs):
        super().__init__(**kwargs)

        self.username = username
        self.name = name
        self.title = title
        self.department = department
        self.company = company
        self.last_seen = last_seen

    @classmethod
    def model(cls, name='User'):
        model = super().model(name)
        model.update({
            'username': fields.String,
            'name': fields.String,
            'title': fields.String,
            'department': fields.String,
            'company': fields.String,
            'last_seen': fields.String,
        })

        return model

@collection
class Job(BaseModel):

    def __init__(self, pid=None, status=None, info=None, **kwargs):
        super().__init__(**kwargs)

        self.pid = pid
        self.status = status
        self.info = info

    @classmethod
    def model(cls, name='Job'):
        model = super().model(name)
        model.update({
            'pid': fields.String,
            'status': fields.String,
            'info': fields.String,
        })

        return model