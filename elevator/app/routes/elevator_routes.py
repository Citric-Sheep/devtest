import json
import http.client

from flask import Response, Blueprint, request
from elevator.elevator import current_elevator

elevator_api_routes = Blueprint("elevator_api", __name__, url_prefix="/api")


@elevator_api_routes.route('/elevators', methods=["POST", "GET"], endpoint="create_or_get_elevators")
def create_or_get_elevators():
    if request.method == "POST":

        top_floor = request.form.get("top_floor")
        lower_floor = request.form.get("lower_floor")

        if not top_floor or not lower_floor:
            return Response(status=http.client.BAD_REQUEST)

        elevator_id = current_elevator.create_elevator(top_floor, lower_floor, set_as_default=True)

        return Response(json.dumps({'elevator_id': elevator_id}),
                        status=http.client.CREATED,
                        mimetype='application/json')
    else:
        elevators = current_elevator.get_elevators()
        return Response(json.dumps(elevators),
                        status=http.client.OK,
                        mimetype='application/json')


@elevator_api_routes.route('/elevators/records/<int:elevator_id>', methods=["GET"])
def get_elevator_records_by_id(elevator_id):
    elevator_records = current_elevator.get_elevator_records_by_elevator_id(elevator_id)
    return Response(json.dumps(elevator_records),
                    status=http.client.OK,
                    mimetype='application/json')


@elevator_api_routes.route('/elevators/call', methods=["POST"], endpoint="call_elevator")
def call_elevator():
    call_floor = request.form.get("call_floor", type=int)
    direction = request.form.get("direction", type=int)

    if not call_floor or not direction:
        return Response(status=http.client.BAD_REQUEST)

    call_record_id = current_elevator.perform_call_movement(call_floor, direction)

    return Response(json.dumps({'elevator_record_id': call_record_id}),
                    status=http.client.CREATED,
                    mimetype='application/json')


@elevator_api_routes.route('/elevators/move', methods=["POST"], endpoint="move_elevator")
def move_elevator():

    target_floor = request.form.get("target_floor", type=int)

    if not target_floor:
        return Response(status=http.client.BAD_REQUEST)

    move_record_id = current_elevator.perform_elevator_movement(target_floor)

    if not move_record_id:
        return Response(json.dumps({'error': "You probably call the elevator to up/down and select the the opposite"}),
                        status=http.client.BAD_REQUEST)

    return Response(json.dumps({'move_record_id': move_record_id}),
                    status=http.client.CREATED,
                    mimetype='application/json')
