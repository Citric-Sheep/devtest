"""
In this file you'll find all controllers related to building endpoints.
"""

from typing import Tuple
from utils.db import PostgreSQLHandler
from models.models import Building
from flask import jsonify, Response
from utils.serializer import serialize_model


__all__ = (
    "get_buildings_controller",
    "create_building_controller",
    "delete_building_controller",
    "update_building_controller"
)


def create_building_controller(data: dict) -> Tuple[str, int]:
    """
    Function that handles /building/create request
    :param data: dictionary that was passed as body in the request.
    :return result, status_code: Tuple with the information related to create execution
    """
    new_building = Building(**data)
    psql = PostgreSQLHandler()
    result = psql.create(new_building)
    status_code = 201 if "Success" in result else 500
    return result, status_code


def get_buildings_controller(building_data: dict = None) -> Response:
    """
    Function that handles /building/get request
    :param building_data: dictionary that was passed as body in the request.
    :return result, status_code: Tuple with the information related to the get execution
    """
    psql = PostgreSQLHandler()
    buildings = psql.read(Building, filter_by=building_data)
    return jsonify([serialize_model(building) for building in buildings])


def update_building_controller(data: dict) -> Tuple[str, int]:
    """
    Function that handles /building/update request
    :param data: dictionary that was passed as body in the request.
    :return result, status_code: Tuple with the information related to the update execution
    """
    psql = PostgreSQLHandler()
    result = psql.update(Building, {"id": data["id"]}, data["new_values"])
    status_code = 500 if "sql" in result.lower() else 200
    return result, status_code


def delete_building_controller(data: dict) -> Tuple[str, int]:
    """
    Function that handles /building/delete request
    :param data: dictionary that was passed as body in the request.
    :return result, status_code: Tuple with the information related to delete execution
    """
    psql = PostgreSQLHandler()
    result = psql.delete(Building, data)
    status_code = 500 if "sql" in result.lower() else 200
    return result, status_code
