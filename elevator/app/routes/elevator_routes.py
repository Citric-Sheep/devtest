import json
import http.client

from flask import Response, Blueprint, redirect, render_template, request, url_for
from elevator.elevator import current_elevator


elevator_routes = Blueprint("elevator", __name__)
elevator_api_routes = Blueprint("elevator_api", __name__, url_prefix="/api")
ELEVATOR_ROW_FLOORS = 3


@elevator_routes.route("/elevator", methods=["POST", "GET"], endpoint="elevator")
def elevator_page():
    if current_elevator.current_elevator_id != 0:
        elevator_floors = list(range(int(current_elevator.lower_floor), int(current_elevator.top_floor) + 1))
        elevator_floors.remove(0)
        elevator_floors_extra_row = int(bool(len(elevator_floors) % ELEVATOR_ROW_FLOORS))
        elevator_rows_floors = len(elevator_floors) // ELEVATOR_ROW_FLOORS + elevator_floors_extra_row
        
        current_elevator.elevator_page_args = {
            **current_elevator.elevator_page_args,
            'elevator_floor': current_elevator.elevator_floor,
            'current_floor': current_elevator.current_floor,
            'elevator_floors': elevator_floors,
            'elevator_row_floors': ELEVATOR_ROW_FLOORS,
            'elevator_rows_floors': elevator_rows_floors
        }
        # current_elevator.get_elevator(set_as_default=True)
        # TODO: Reverse list
        return render_template("index.html", elevator_page_args=current_elevator.elevator_page_args)
    return render_template("index.html", elevator_page_args=current_elevator.elevator_page_args)


@elevator_routes.route("/elevator/current_floor",  methods=["POST"], endpoint="set_elevator_current_floor")
def set_elevator_current_floor():

    print(request.form.keys)
    floor_number = request.form.get("floor_number")

    if not floor_number:
        return Response(status=http.client.BAD_REQUEST)

    current_elevator.elevator_page_args = {
        **current_elevator.elevator_page_args,
        'current_floor': floor_number,
    }
    current_elevator.current_floor = floor_number
    return render_template("index.html", elevator_page_args=current_elevator.elevator_page_args)


# API METHODS
@elevator_api_routes.route('/elevators', methods=["POST", "GET"], endpoint="create_or_get_elevators")
def create_or_get_elevators():
    if request.method == "POST":

        top_floor = request.form.get("top_floor")
        lower_floor = request.form.get("lower_floor")

        if not top_floor or not lower_floor:
            return Response(status=http.client.BAD_REQUEST)

        elevator_id = current_elevator.create_elevator(top_floor, lower_floor, set_as_default=True)

        elevator_creation_page = url_for('elevator.elevator')
        if request.referrer and request.referrer.endswith(elevator_creation_page):
            return redirect(elevator_creation_page)

        return Response(json.dumps({'elevator_id': elevator_id}),
                        status=http.client.CREATED,
                        mimetype='application/json')
    else:
        current_elevator.get_elevators()
        return ""


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


@elevator_api_routes.route('/elevators/records', methods=["GET"])
def get_elevator_records_by_id():
    """"""
