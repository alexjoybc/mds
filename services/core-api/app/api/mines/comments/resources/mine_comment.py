import uuid
from flask_restplus import Resource, reqparse, fields, inputs
from flask import request, current_app
from datetime import datetime
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError
from sqlalchemy.exc import DBAPIError

from app.extensions import api, db
from app.api.utils.custom_reqparser import CustomReqparser
from app.api.utils.resources_mixins import UserMixin
from app.api.utils.access_decorators import requires_role_view_all, requires_role_mine_edit, requires_role_mine_admin

from app.api.mines.mine.models.mine import Mine
from app.api.mines.comments.models.mine_comment import MineComment

from app.api.mines.response_models import MINE_COMMENT_MODEL


class MineCommentListResource(Resource, UserMixin):
    parser = CustomReqparser()
    parser.add_argument('mine_comment', type=str, location='json')

    @api.doc(description='retrive a list of comments for amine')
    @api.marshal_with(MINE_COMMENT_MODEL, envelope='records', code=200)
    @requires_role_view_all
    def get(self, mine_guid):

        mine = Mine.find_by_mine_guid(mine_guid)

        if not mine:
            raise NotFound('Mine not found')

        current_app.logger.info(f'Retrieving comments for {mine}')

        comments = [comment.__dict__ for comment in mine.comments]

        return comments, 200

    @api.expect(MINE_COMMENT_MODEL)
    @api.doc(description='creates a new comment for the Mine')
    @api.marshal_with(MINE_COMMENT_MODEL, code=201)
    @requires_role_mine_edit
    def post(self, mine_guid):

        mine = Mine.find_by_mine_guid(mine_guid)

        if not mine:
            raise NotFound('Mine not found')

        data = self.parser.parse_args()

        if not data['mine_comment']:
            raise BadRequest('Empty comment')

        mine_comment = MineComment.create(
            mine=mine,
            mine_comment=data['mine_comment'],
        )

        current_app.logger.info(f'Creating comment {mine_comment}')

        mine_comment.save()

        return mine_comment, 201


class MineCommentResource(Resource, UserMixin):
    parser = CustomReqparser()
    parser.add_argument('report_comment', type=str, location='json')
    parser.add_argument('comment_visibility_ind', type=inputs.boolean, location='json')

    # @api.expect(MINE_REPORT_COMMENT_MODEL)
    # @api.doc(description='update a comment')
    # @api.marshal_with(MINE_REPORT_COMMENT_MODEL, code=201)
    # @requires_role_mine_edit
    # def put(self, mine_guid, mine_report_guid, mine_report_comment_guid=None):

    #     data = self.parser.parse_args()
    #     comment = MineReportComment.find_by_guid(mine_report_comment_guid)
    #     if not comment:
    #         raise NotFound('Mine report comment with guid "{mine_report_comment_guid}" not found.')

    #     current_app.logger.info(f'Updating {comment} with {data}')
    #     for key, value in data.items():
    #         setattr(comment, key, value)

    #     comment.save()

    #     return comment, 201

    # @api.doc(
    #     description='Delete a mine report comment by guid',
    #     params={'mine_report_comment_guid': 'guid of the comment to delete.'})
    # @requires_role_mine_admin
    # def delete(self, mine_guid, mine_report_guid, mine_report_comment_guid):
    #     comment = MineReportComment.find_by_guid(mine_report_comment_guid)
    #     if not comment:
    #         raise NotFound('Mine report comment with guid "{mine_report_comment_guid}" not found.')

    #     comment.deleted_ind = True
    #     current_app.logger.info(f'Deleting {comment}')

    #     comment.save()

    #     return ('', 204)
