from bson import ObjectId
from flask_restx import fields, Model

from api import db


class BaseModel:
    def __init__(self, **kwargs):
        [self.__setattr__(k, v) for k, v in kwargs.items()]

    def get_id(self):
        return self._id if hasattr(self, '_id') else None

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

    def in_db(obj):
        res = obj.__collection__.find_one({'_id': obj.get_id()})
        return res

    def insert(obj):
        _id = obj.__collection__.insert_one(vars(obj)).inserted_id
        setattr(obj, '_id', _id)
        return obj

    def update(obj):
        obj.__collection__.replace_one({'_id': obj._id}, vars(obj))

    def delete(obj):
        return obj.__collection__.delete_one({'_id': obj._id}).deleted_count

    setattr(cls, '__collection__', db[f'{cls.__name__.lower()}s'])
    setattr(cls, 'in_db', in_db)
    setattr(cls, 'insert', insert)
    setattr(cls, 'update', update)
    setattr(cls, 'delete', delete)

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
