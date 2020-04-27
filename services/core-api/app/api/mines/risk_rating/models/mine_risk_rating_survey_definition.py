from sqlalchemy.schema import FetchedValue
from app.api.utils.models_mixins import Base
from app.extensions import db


class MineRiskRatingSurveyDefinition(Base):
    __tablename__ = 'mine_risk_rating_survey_definition'

    mine_risk_rating_survey_definition_id = db.Column(db.Integer, primary_key=True)
    survey_definition_json = db.Column(db.String, nullable=False)
    is_active_survey = db.Column(db.Boolean, nullable=False, server_default=FetchedValue())
    create_timestamp = db.Column(db.DateTime, nullable=False, server_default=FetchedValue())

    def __repr__(self):
        return '<MineRiskRatingSurveyDefinition %r>' % self.mine_risk_rating_survey_definition_id

    @classmethod
    def get_active(cls):
        return cls.query.all()
