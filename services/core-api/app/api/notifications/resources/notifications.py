from flask_restplus import Resource
from flask import request
from werkzeug.exceptions import BadRequest, NotFound

from app.extensions import api
from app.api.utils.access_decorators import requires_role_view_all
from app.api.utils.resources_mixins import UserMixin

from datetime import datetime

from app.api.notifications.response_models import NOTIFICATION_MODEL


class NotificationsResource(Resource):
    #@requires_role_view_all
    @api.doc(description='Get your notification feed')
    @api.marshal_with(NOTIFICATION_MODEL, code=200)
    def get(self):

        response = []
        response.append({
            'read': False,
            'avatar': "avatar url",
            'key': "key.in.redis",
            'title': "CRR Submission",
            'description': "A CRR submission was performed by Mine ABC",
            'date': datetime.now(),
            'link': "/core/relative/link"
        })

        return response
        # feed = notifications.get_feeds()['normal']
        # activities = list(feed[:25])
        # return activities
