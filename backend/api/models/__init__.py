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

