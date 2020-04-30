from app.extensions import api
from flask_restplus import fields

NOTIFICATION_MODEL = api.model(
    'Notification', {
        'read': fields.Boolean,
        'avatar': fields.String,
        'key': fields.String,
        'title': fields.String,
        'description': fields.String,
        'date': fields.Date,
        'link': fields.String
    })
