from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.associationproxy import association_proxy

from app.api.utils.models_mixins import Base, AuditMixin
from app.extensions import db
from app.api.constants import *


class PermitCondition(Base, AuditMixin):
    __tablename__ = "permit_condition"

    permit_condition_id = db.Column(db.Integer, primary_key=True)
    now_application_id = db.Column(
        db.Integer, db.ForeignKey('now_application.now_application_id'), nullable=False)
    now_application = db.relationship('NOWApplication', backref='permit_conditions')

    condition_section = db.Column(db.String, nullable=False)
    condition_text = db.Column(db.String, nullable=False)
    condition_start_date = db.Column(db.String, nullable=False)
    #library_condition_id = db.Column(db.Integer, db.ForeignKey())
    active_ind = db.Column(db.Boolean, nullable=False, server_default=FetchedValue())

    def __repr__(self):
        return '<PermitCondition %r>' % self.permit_condition_id
