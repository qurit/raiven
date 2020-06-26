from flask_restx import fields

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

