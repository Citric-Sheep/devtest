"""
In this file you'll find all controllers related to demand endpoints.
"""

from utils.db import PostgreSQLHandler
from models.models import Demand
from flask import jsonify, Response
from typing import Tuple
from utils.serializer import serialize_model


__all__ = (
    "get_demand_controller",
    "create_demand_controller",
    "update_demand_controller",
    "delete_demand_controller"
    )


def create_demand_controller(data: dict) -> Tuple[str, int]:
    """
    Function that handles /demand/create request
    :param data: dictionary that was passed as body in the request.
    :return result, status_code: Tuple with the information related to create execution
    """
    new_demand = Demand(**data)
    psql = PostgreSQLHandler()
    result = psql.create(new_demand)
    status_code = 201 if "Success" in result else 500
    return result, status_code


def get_demand_controller(elevator_id: int = None) -> Response:
    """
    Function that handles /demand/get request
    :param elevator_id: dictionary with the id that was received in query params.
    :return result, status_code: Tuple with the information related to get execution
    """
    psql = PostgreSQLHandler()
    demands = psql.read(Demand, filter_by={"id": elevator_id} if elevator_id else None)
    return jsonify([serialize_model(demand) for demand in demands])


def update_demand_controller(data: dict) -> Tuple[str, int]:
    """
    Function that handles /demand/update request
    :param data: dictionary that was passed as body in the request.
    :return result, status_code: Tuple with the information related to update execution
    """
    psql = PostgreSQLHandler()
    result = psql.update(Demand, {"id": data["id"]}, data["new_values"])
    status_code = 500 if "sql" in result.lower() else 200
    return result, status_code


def delete_demand_controller(data: dict) -> Tuple[str, int]:
    """
    Function that handles /demand/delete request
    :param data: dictionary that was passed as body in the request.
    :return result, status_code: Tuple with the information related to delete execution
    """
    psql = PostgreSQLHandler()
    result = psql.delete(Demand, data)
    status_code = 500 if "sql" in result.lower() else 200
    return result, status_code
