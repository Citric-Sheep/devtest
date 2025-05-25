# -*- coding: utf-8 -*-
from flask import request
from app import app
from app.crud import create_demand,create_state,change_state

@app.route('/demand', methods=['POST'])
def create_demand_view():
    try:
        data = request.json
        create_demand(data)
        return {'message': 'Demand created'}, 201
    except Exception as e:
        return {'message':f'{e.str()}'},404

@app.route('/state', methods=['POST'])
def create_state_view():
    try:
        data = request.json
        create_state(data)
        return {'message': 'State created'}, 201
    except Exception as e:
        return {'message':f'{e.str()}'},404

@app.route('/state/<state_id>/end',methods=["PATCH"])
def change_state_view(state_id):
    data = request.json
    result = change_state(state_id,data)
    if not result:
        return {"message":"No state found"},404
    return {"message":"State changed"},201
    
    