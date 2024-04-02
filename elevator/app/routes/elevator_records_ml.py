import json
import http.client

from flask import Response, Blueprint, redirect, render_template, request, url_for
from elevator import elevator_records_ml_functions


elevator_records_ml = Blueprint("elevator_records_ml", __name__, url_prefix="/api/elevator_records_ml")


@elevator_records_ml.route("/get_ml_records/<int:elevator_id>", methods=["GET"])
def get_elevator_records_ml(elevator_id):
    current_elevator_records = elevator_records_ml_functions.get_records_by_elevator_id_with_resting_floor_calculated(
        elevator_id)
    return Response(json.dumps(current_elevator_records),
                    status=http.client.OK,
                    mimetype='application/json')
