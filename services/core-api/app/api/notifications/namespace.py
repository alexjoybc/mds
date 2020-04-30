from flask_restplus import Namespace

from app.api.notifications.resources.notifications import NotificationsResource

api = Namespace('notifications', description='Core notifications')

api.add_resource(NotificationsResource, '')
