from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.inspection import inspect

from app.api.utils.models_mixins import Base
from app.extensions import db


class ExemptionFeeStatusCSVView(Base):
    __tablename__ = "exemption_fee_status_view"
    mine_guid = db.Column(UUID(as_uuid=True), primary_key=True)
    permit_guid = db.Column(UUID(as_uuid=True), primary_key=True)
    mine_no = db.Column(db.String)
    permit_no = db.Column(db.String)
    mine_name = db.Column(db.String)
    exemption_fee_status_code = db.Column(db.String)
    exemption_fee_status_description = db.Column(db.String)
    exemption_fee_status_note = db.Column(db.String)
    mine_owner_name = db.Column(db.String)
    address_line_1 = db.Column(db.String)
    address_line_2 = db.Column(db.String)
    city = db.Column(db.String)
    sub_division_code = db.Column(db.String)
    post_code = db.Column(db.String)

    def csv_row(self):
        model = inspect(self.__class__)
        return "\"" + '","'.join([(str(getattr(self, c.name)) or "").rstrip(',')
                                  for c in model.columns]) + "\""
