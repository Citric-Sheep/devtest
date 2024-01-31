from sanic import Blueprint
from sanic.response import json

from src.gateway.database.demand_log_database import DemandLogDatabase
from src.gateway.database.elevator_database import ElevatorDatabase

elevator_bp = Blueprint("elevators", url_prefix="elevators", version=1)


@elevator_bp.route("/", methods=["GET"])
async def get_elevators_request(request):
    elevators = ElevatorDatabase.get_all()
    elevators = [elevator.dict() for elevator in elevators]
    return json(elevators, status=200)


@elevator_bp.route("/logs", methods=["GET"])
async def get_elevators_logs_request(request):
    logs = DemandLogDatabase.get_all()
    logs = [log.dict() for log in logs]
    return json(logs, status=200)


@elevator_bp.route("/<elevator_id>", methods=["GET"])
async def get_elevator_request(request, elevator_id):
    elevator = ElevatorDatabase.get_by_id(elevator_id)
    if elevator is None:
        return json({"message": "Elevator not found"}, status=404)

    return json(elevator.dict(), status=200)


@elevator_bp.route("/<elevator_id>", methods=["PUT"])
async def update_elevator_request(request, elevator_id):
    elevator = ElevatorDatabase.get_by_id(elevator_id)
    if elevator is None:
        return json({"message": "Elevator not found"}, status=404)

    elevator.name = request.json.get("name")
    ElevatorDatabase.update(elevator)
    return json(elevator.dict(), status=200)


@elevator_bp.route("/<elevator_id>", methods=["DELETE"])
async def delete_elevator_request(request, elevator_id):
    ElevatorDatabase.delete(elevator_id)
    return json({"message": "Elevator deleted"}, status=200)


@elevator_bp.route("/<elevator_id>/log", methods=["GET"])
async def get_log_elevator_request(request, elevator_id):
    logs = DemandLogDatabase.get_by_elevator_id(elevator_id)
    logs = [log.dict() for log in logs]
    return json(logs, status=200)
