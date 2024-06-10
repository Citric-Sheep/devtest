from datetime import datetime
from flask import jsonify, request
from models import db, ElevatorDemand, ElevatorRestFloor
from rules.floorRule import checkData  # checarDados -> checkData

def register_elevator_demand():  # registrar_demanda_elevador -> register_elevator_demand
    data = request.get_json()
    if checkData(data):
        new_demand = ElevatorDemand(  # nova_demanda -> new_demand
            elevator_id=data['elevator_id'],
            floor_id=data['floor_id'],  # andar_id -> floor_id
            timestamp=datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%SZ'),
            direction=data['direction'],  # direcao -> direction
            request_type=data['types']  # tipo -> type
        )
        db.session.add(new_demand)
        db.session.commit()
        return jsonify({"message": "Demand registered"}), 201  # mensagem -> message
    else:
        return jsonify({"message": "Floor does not exist"}), 404  # mensagem -> message

def register_elevator_rest_floor():  # registrar_andar_repouso_elevador -> register_elevator_rest_floor
    data = request.get_json()
    new_rest_floor = ElevatorRestFloor(  # novo_andar_repouso -> new_rest_floor
        elevator_id=data['elevator_id'],
        floor_id=data['floor_id'],  # andar_id -> floor_id
        timestamp=datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%SZ'),
        reason=data['reason']  # motivo -> reason
    )
    db.session.add(new_rest_floor)
    db.session.commit()
    return jsonify({"message": "Rest floor registered"}), 201  # mensagem -> message

def get_elevator_demands():  # get_demandas_elevador -> get_elevator_demands
    demands = ElevatorDemand.query.all()  # demandas -> demands
    serialized_demands = []  # demandas_serializadas -> serialized_demands
    for demand in demands:  # demanda -> demand
        serialized_demand = {  # demanda_serializada -> serialized_demand
            'demand_id': demand.demand_id,
            'timestamp': demand.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'floor_id': demand.floor_id,  # andar_id -> floor_id
            'elevator_id': demand.elevator_id,
            'direction': demand.direction,  # direcao -> direction
            'request_type': demand.request_type  # tipo -> type
        }
        serialized_demands.append(serialized_demand)
    return jsonify(serialized_demands), 200

def get_elevator_demands_by_floor(floor_id):  # get_demandas_elevador_por_andar -> get_elevator_demands_by_floor
    demands = ElevatorDemand.query.filter_by(floor_id=floor_id).all()  # demandas -> demands
    if not demands:
        return jsonify({"message": f"No demands found for the floor with ID '{floor_id}'"}), 404  # mensagem -> message
    
    serialized_demands = []  # demandas_serializadas -> serialized_demands
    for demand in demands:  # demanda -> demand
        serialized_demand = {  # demanda_serializada -> serialized_demand
            'demand_id': demand.demand_id,
            'timestamp': demand.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'floor_id': demand.floor_id,  # andar_id -> floor_id
            'elevator_id': demand.elevator_id,
            'direction': demand.direction,  # direcao -> direction
            'request_type': demand.request_type  # tipo -> type
        }
        serialized_demands.append(serialized_demand)
    return jsonify(serialized_demands), 200
