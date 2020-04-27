from flask import Response, current_app
from flask_restplus import Resource
from sqlalchemy.inspection import inspect

from app.api.exports.exemption_fee_status.models.exemption_fee_status_csv_view import ExemptionFeeStatusCSVView

from app.extensions import api, cache
from app.api.utils.access_decorators import requires_role_view_all


class ExemptionFeeStatusCSVResource(Resource):
    @api.doc(
        description=
        'Returns exemtion fee status and mine details in a CSV.'
    )
    #@requires_role_view_all
    def get(self):
    
        model = inspect(ExemptionFeeStatusCSVView)

        csv_string = "\"" + '","'.join([c.name or "" for c in model.columns]) + "\"\n"

        rows = ExemptionFeeStatusCSVView.query.all()

        csv_string += '\n'.join([r.csv_row() for r in rows])

        return Response(csv_string, mimetype='text/csv')
