from app.api.utils.models_mixins import Base
from app.extensions import db


class MMSPlacerActivity(Base):
    __tablename__ = "placer_activity"
    __table_args__ = {"schema": "mms_now_submissions"}
    placeractivityid = db.Column(db.Integer, primary_key=True)
    messageid = db.Column(db.Integer, db.ForeignKey('mms_now_submissions.application.messageid'))
    mms_cid = db.Column(db.Integer)
    type = db.Column(db.String)
    quantity = db.Column(db.Integer)
    disturbedarea = db.Column(db.Numeric(14, 2))
    timbervolume = db.Column(db.Numeric(14, 2))

    def __repr__(self):
        return '<MMSPlacerActivity %r>' % self.id
