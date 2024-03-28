"""
In this file you'll find all controllers related to elevator endpoints.
"""

from utils.db import PostgreSQLHandler
from models.models import Elevator
from flask import jsonify, Response
from utils.serializer import serialize_model


__all__ = (
    "get_elevators_controller",
    "create_elevator_controller",
    "update_elevator_controller",
    "delete_elevator_controller",
    )


def create_elevator_controller(data):
    """
    Function that handles /elevator/create request
    :param data: dictionary that was passed as body in the request.
    :return result, status_code: Tuple with the information related to create execution
    """
    new_elevator = Elevator(**data)
    psql = PostgreSQLHandler()
    result = psql.create(new_elevator)
    status_code = 201 if "Success" in result else 500
    return result, status_code


def get_elevators_controller(elevator_id: int = None) -> Response:
    """
    Function that handles /elevator/get request
    :param elevator_id: dictionary that was passed as body in the request.
    :return result, status_code: Tuple with the information related to get execution
    """
    psql = PostgreSQLHandler()
    elevators = psql.read(Elevator, filter_by={"id": elevator_id} if elevator_id else None)
    return jsonify([serialize_model(elevator) for elevator in elevators])


def update_elevator_controller(data):
    """
    Function that handles /elevator/update request
    :param data: dictionary that was passed as body in the request.
    :return result, status_code: Tuple with the information related to update execution
    """
    psql = PostgreSQLHandler()
    result = psql.update(Elevator, {"id": data["id"]}, data["new_values"])
    status_code = 500 if "sql" in result.lower() else 200
    return result, status_code


def delete_elevator_controller(data):
    """
    Function that handles /elevator/delete request
    :param data: dictionary that was passed as body in the request.
    :return result, status_code: Tuple with the information related to delete execution
    """
    psql = PostgreSQLHandler()
    result = psql.delete(Elevator, data)
    status_code = 500 if "sql" in result.lower() else 200
    return result, status_code
