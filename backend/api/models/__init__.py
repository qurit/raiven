from bson import ObjectId
from flask_restx import fields, Model

from api import db


def collection(cls):

    def save(self):
        return self.company

    setattr(cls, '__table__', f'{cls.__name__}s')
    setattr(cls, 'save', save)
    return cls


class BaseModel:
    def __init__(self, **kwargs):
        [self.__setattr__(k, v) for k, v in kwargs.items()]

    def save(self):
        return self.__collection__.insert_one(vars(self), {})

    @classmethod
    def model(cls, name='Base'):
        return Model(name, {'_id': fields.String})

    @classmethod
    def list_model(cls):
        m = cls.model()
        return Model(f'{m.name} list', {f'{m.name}s': fields.List(fields.Nested(m))})


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


job = (
    'Job',
    {
        '_id': fields.String,
        'pid': fields.String,
        'status': fields.String,
        'info': fields.String,
    }
)

user = (
    'User',
    {
        '_id': fields.String,
        'username': fields.String,
        'name': fields.String,
        'title': fields.String,
        'department': fields.String,
        'company': fields.String,
        'last_seen': fields.String,
    }
)

if __name__ == '__main__':
    # job = Job('xyz', status='Queued', info='15 Second Test Func')
    # User().save()
    print(User().save())