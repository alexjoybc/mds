from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import FetchedValue
from app.api.utils.models_mixins import Base
from app.extensions import db


class MineRiskRatingSurveyResponse(Base):
    __tablename__ = 'mine_risk_rating_survey_response'

    mine_risk_rating_survey_response_id = db.Column(db.Integer, primary_key=True)
    mine_risk_rating_survey_definition_id = db.Column(
        db.Integer,
        db.ForeignKey('mine_risk_rating_survey_definition.mine_risk_rating_survey_definition_id'))
    mine_guid = db.Column(UUID(as_uuid=True), db.ForeignKey('mine.mine_guid'))
    survey_response_json = db.Column(db.String, nullable=False)
    notes = db.Column(db.String, nullable=True)
    username = db.Column(db.String, nullable=False)
    rating = db.Column(db.Numeric(5, 2), nullable=False)
    create_timestamp = db.Column(db.DateTime, nullable=False, server_default=FetchedValue())

    def __repr__(self):
        return '<MineRiskRatingSurveyResponse %r>' % self.mine_risk_rating_survey_response_id

    @classmethod
    def find_by_mine_guid(cls, mine_guid):
        return cls.query.filter_by(mine_guid=mine_guid).all()
