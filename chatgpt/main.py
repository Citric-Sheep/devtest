from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import sqlite3
import os
from typing import Dict, List, Optional
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elevator_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key'

db = SQLAlchemy(app)

class Building(db.Model):
    __tablename__ = 'buildings'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    total_floors = db.Column(db.Integer, nullable=False)
    building_type = db.Column(db.String(50)) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    elevators = db.relationship('Elevator', backref='building', lazy=True)

class Elevator(db.Model):
    __tablename__ = 'elevators'
    
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False)
    elevator_number = db.Column(db.String(10), nullable=False)
    max_capacity = db.Column(db.Integer, default=1000)  
    current_floor = db.Column(db.Integer, default=1)
    current_load = db.Column(db.Integer, default=0) 
    is_moving = db.Column(db.Boolean, default=False)
    maintenance_status = db.Column(db.String(20), default='operational')
    last_maintenance = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    calls = db.relationship('ElevatorCall', backref='elevator', lazy=True)

class ElevatorCall(db.Model):
    __tablename__ = 'elevator_calls'
    
    id = db.Column(db.Integer, primary_key=True)
    elevator_id = db.Column(db.Integer, db.ForeignKey('elevators.id'), nullable=False)
    called_from_floor = db.Column(db.Integer, nullable=False)
    destination_floor = db.Column(db.Integer)
    call_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    response_time = db.Column(db.Float)  
    elevator_position_at_call = db.Column(db.Integer)  
    estimated_passengers = db.Column(db.Integer, default=1)
    call_type = db.Column(db.String(20), default='normal') 
    day_of_week = db.Column(db.Integer) 
    hour_of_day = db.Column(db.Integer)
    week_of_month = db.Column(db.Integer)
    season = db.Column(db.String(10))
    weather_condition = db.Column(db.String(20))  
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        call_dt = self.call_time or datetime.utcnow()
        self.day_of_week = call_dt.weekday()
        self.hour_of_day = call_dt.hour
        self.week_of_month = (call_dt.day - 1) // 7 + 1
        self.season = self._get_season(call_dt.month)
    
    def _get_season(self, month: int) -> str:
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        else:
            return 'autumn'

class ElevatorBusinessRules:
    @staticmethod
    def validate_floor_range(floor: int, building_id: int) -> bool:
        """Validate if a floor number is valid for a given building."""
        building = Building.query.get(building_id)
        if not building:
            return False
        return 1 <= floor <= building.total_floors

    @staticmethod
    def can_elevator_access_floor(elevator_id: int, floor: int) -> bool:
        """Check if an elevator can access a specific floor."""
        elevator = Elevator.query.get(elevator_id)
        if not elevator:
            return False
        
        if not ElevatorBusinessRules.validate_floor_range(floor, elevator.building_id):
            return False
        
        if elevator.elevator_number == "FREIGHT" and floor > 5:
            return False
        
        return True

    @staticmethod
    def calculate_response_time(call_time: datetime, elevator_position: int, called_floor: int) -> float:
        floors_to_travel = abs(elevator_position - called_floor)
        return floors_to_travel * 3.0 + 2.0
    
    @staticmethod
    def should_trigger_maintenance_alert(elevator: Elevator) -> bool:
        if not elevator.last_maintenance:
            return True
        days_since_maintenance = (datetime.utcnow() - elevator.last_maintenance).days
        return days_since_maintenance > 30

@app.route('/api/buildings', methods=['POST'])
def create_building():
    """Create a new building"""
    data = request.get_json()
    
    if not data or 'name' not in data or 'total_floors' not in data:
        return jsonify({'error': 'Missing required fields: name, total_floors'}), 400
    
    building = Building(
        name=data['name'],
        total_floors=data['total_floors'],
        building_type=data.get('building_type', 'mixed')
    )
    
    try:
        db.session.add(building)
        db.session.commit()
        return jsonify({
            'id': building.id,
            'name': building.name,
            'total_floors': building.total_floors,
            'building_type': building.building_type
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/buildings/<int:building_id>/elevators', methods=['POST'])
def create_elevator(building_id):
    """Add an elevator to a building"""
    data = request.get_json()
    
    if not data or 'elevator_number' not in data:
        return jsonify({'error': 'Missing required field: elevator_number'}), 400
    
    elevator = Elevator(
        building_id=building_id,
        elevator_number=data['elevator_number'],
        max_capacity=data.get('max_capacity', 1000),
        current_floor=data.get('current_floor', 1)
    )
    
    try:
        db.session.add(elevator)
        db.session.commit()
        return jsonify({
            'id': elevator.id,
            'elevator_number': elevator.elevator_number,
            'current_floor': elevator.current_floor,
            'building_id': building_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/elevators/<int:elevator_id>/call', methods=['POST'])
def record_elevator_call(elevator_id):
    """Record an elevator call """
    elevator = Elevator.query.get_or_404(elevator_id)
    data = request.get_json()
    
    if not data or 'called_from_floor' not in data:
        return jsonify({'error': 'Missing required field: called_from_floor'}), 400
    
    called_from_floor = data['called_from_floor']
    
    if not ElevatorBusinessRules.validate_floor_range(called_from_floor, elevator.building_id):
        return jsonify({'error': 'Invalid floor number'}), 400
    
    response_time = ElevatorBusinessRules.calculate_response_time(
        datetime.utcnow(), elevator.current_floor, called_from_floor
    )
    
    call = ElevatorCall(
        elevator_id=elevator_id,
        called_from_floor=called_from_floor,
        destination_floor=data.get('destination_floor'),
        elevator_position_at_call=elevator.current_floor,
        response_time=response_time,
        estimated_passengers=data.get('estimated_passengers', 1),
        call_type=data.get('call_type', 'normal'),
        weather_condition=data.get('weather_condition')
    )
    
    try:
        db.session.add(call)
        db.session.commit()
        
        if data.get('destination_floor'):
            elevator.current_floor = data['destination_floor']
            elevator.is_moving = False
            db.session.commit()
        
        return jsonify({
            'call_id': call.id,
            'estimated_response_time': response_time,
            'call_time': call.call_time.isoformat(),
            'temporal_features': {
                'day_of_week': call.day_of_week,
                'hour_of_day': call.hour_of_day,
                'week_of_month': call.week_of_month,
                'season': call.season
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/elevators/<int:elevator_id>/status', methods=['GET'])
def get_elevator_status(elevator_id):
    """Get current elevator status"""
    elevator = Elevator.query.get_or_404(elevator_id)
    
    maintenance_alert = ElevatorBusinessRules.should_trigger_maintenance_alert(elevator)
    
    return jsonify({
        'elevator_id': elevator.id,
        'elevator_number': elevator.elevator_number,
        'current_floor': elevator.current_floor,
        'current_load': elevator.current_load,
        'is_moving': elevator.is_moving,
        'maintenance_status': elevator.maintenance_status,
        'maintenance_alert': maintenance_alert,
        'building_id': elevator.building_id,
        'max_floors': elevator.building.total_floors
    })

@app.route('/api/ml-data/features/<int:building_id>', methods=['GET'])
def get_ml_features(building_id):
    """Get data formatted for ML training"""
    building = Building.query.get_or_404(building_id)
    
    days_back = request.args.get('days_back', 30, type=int)
    include_weather = request.args.get('include_weather', False, type=bool)
    
    cutoff_date = datetime.utcnow() - timedelta(days=days_back)
    
    calls_query = db.session.query(ElevatorCall).join(Elevator).filter(
        Elevator.building_id == building_id,
        ElevatorCall.call_time >= cutoff_date
    ).all()
    
    features = []
    for call in calls_query:
        feature_row = {
            'target_floor': call.called_from_floor, 
            'time_features': {
                'hour_of_day': call.hour_of_day,
                'day_of_week': call.day_of_week,
                'week_of_month': call.week_of_month,
                'season': call.season
            },
            'elevator_features': {
                'elevator_position_at_call': call.elevator_position_at_call,
                'estimated_passengers': call.estimated_passengers,
                'call_type': call.call_type
            },
            'contextual_features': {
                'response_time': call.response_time,
                'building_type': building.building_type,
                'total_floors': building.total_floors
            }
        }
        
        if include_weather and call.weather_condition:
            feature_row['contextual_features']['weather_condition'] = call.weather_condition
        
        features.append(feature_row)
    
    return jsonify({
        'building_id': building_id,
        'total_samples': len(features),
        'date_range': {
            'from': cutoff_date.isoformat(),
            'to': datetime.utcnow().isoformat()
        },
        'features': features
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'database': 'connected'
    })

_initialized = False

@app.before_request
def before_request():
    global _initialized
    if not _initialized:
        db.create_all()
        
        # Create sample data if none exists
        if Building.query.count() == 0:
            sample_building = Building(
                name="Sample Office Building",
                total_floors=10,
                building_type="office"
            )
            db.session.add(sample_building)
            db.session.commit()
            
            sample_elevator = Elevator(
                building_id=sample_building.id,
                elevator_number="ELV-01",
                current_floor=1
            )
            db.session.add(sample_elevator)
            db.session.commit()
        
        _initialized = True

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)