from flask_restplus import Resource

from app.extensions import api
from app.api.utils.access_decorators import requires_role_view_all
from app.api.mines.response_models import MINE_RISK_RATING_SURVEY_DEFINITION_MODEL
from app.api.mines.risk_rating.models.mine_risk_rating_survey_definition import MineRiskRatingSurveyDefinition


class MineRiskRatingSurveyDefinitionResource(Resource):
    @api.doc(description='Get all mine risk rating surveys')
    @api.marshal_with(MINE_RISK_RATING_SURVEY_DEFINITION_MODEL, code=200, envelope='records')
    @requires_role_view_all
    def get(self):
        return MineRiskRatingSurveyDefinition.get_active()
