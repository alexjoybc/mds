from datetime import datetime
from flask import request
from flask_restplus import Resource
from werkzeug.exceptions import BadRequest
from marshmallow.exceptions import MarshmallowError

from app.extensions import api
from app.api.utils.access_decorators import requires_role_view_all, requires_role_mine_edit
from app.api.utils.resources_mixins import UserMixin
from app.api.utils.include.user_info import User
from app.api.mines.risk_rating.models.mine_risk_rating_survey_response import MineRiskRatingSurveyResponse
from app.api.mines.risk_rating.models.mine_risk_rating_survey_response import MineRiskRatingSurveyResponse
from app.api.mines.response_models import MINE_RISK_RATING_SURVEY_RESPONSE_MODEL, MINE_RISK_RATING_SURVEY_RESPONSE_POST_MODEL


class MineRiskRatingSurveyResponseListResource(Resource, UserMixin):
    @api.doc(description='Get all risk rating survey responses')
    # @requires_role_view_all
    @api.marshal_with(MINE_RISK_RATING_SURVEY_RESPONSE_MODEL, code=200)
    def get(self):
        return MineRiskRatingSurveyResponse.query.all()

    @api.doc(description='Create a risk rating survey response')
    # @requires_role_mine_edit
    @api.expect(MINE_RISK_RATING_SURVEY_RESPONSE_POST_MODEL)
    @api.marshal_with(MINE_RISK_RATING_SURVEY_RESPONSE_MODEL, code=201)
    def post(self):
        try:
            mine_risk_rating_survey_response = MineRiskRatingSurveyResponse._schema().load(
                request.json)
        except MarshmallowError as e:
            raise BadRequest(e)

        # Enforce correct username and creation timestamp
        mine_risk_rating_survey_response.username = User().get_user_username()
        mine_risk_rating_survey_response.create_timestamp = datetime.now()
        mine_risk_rating_survey_response.save()

        return mine_risk_rating_survey_response, 201


class MineRiskRatingSurveyResponseResource(Resource, UserMixin):
    @api.doc(description='Get all of a mine\'s risk rating survey responses')
    # @requires_role_view_all
    @api.marshal_with(MINE_RISK_RATING_SURVEY_RESPONSE_MODEL, code=200)
    def get(self, mine_guid):
        return MineRiskRatingSurveyResponse.find_by_mine_guid(mine_guid)
