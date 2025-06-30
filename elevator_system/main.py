from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elevator_prediction.db'
db = SQLAlchemy(app)


class DemandLog(db.Model):
    """Single table for ML training data - captures the 'golden event'"""
    id = db.Column(db.Integer, primary_key=True)
    timestamp_rested = db.Column(db.DateTime, nullable=False)
    timestamp_called = db.Column(db.DateTime, nullable=False)
    resting_floor = db.Column(db.Integer, nullable=False)
    call_floor = db.Column(db.Integer, nullable=False)
    destination_floor = db.Column(db.Integer, nullable=True)
    day_of_week = db.Column(db.Integer, nullable=False)
    hour_of_day = db.Column(db.Integer, nullable=False)


class Elevator:
    """Simple elevator simulation"""
    def __init__(self):
        self.current_floor = 1
        self.direction = 'idle'
        self.is_resting = True
        self.resting_since = None
        self.destination_queue = []
    
    def get_state(self):
        return {
            'current_floor': self.current_floor,
            'direction': self.direction,
            'is_resting': self.is_resting,
            'resting_since': self.resting_since.isoformat() if self.resting_since else None,
            'destination_queue': self.destination_queue
        }
    
    def start_resting(self, timestamp):
        self.is_resting = True
        self.direction = 'idle'
        self.resting_since = timestamp
        self.destination_queue = []
    
    def receive_call(self, call_floor, destination_floor=None):
        if self.is_resting and self.resting_since:
            now = datetime.now()
            day_of_week = now.weekday()
            hour_of_day = now.hour
            
            log_entry = DemandLog(
                timestamp_rested=self.resting_since,
                timestamp_called=now,
                resting_floor=self.current_floor,
                call_floor=call_floor,
                destination_floor=destination_floor,
                day_of_week=day_of_week,
                hour_of_day=hour_of_day
            )
            db.session.add(log_entry)
            db.session.commit()
        
        if call_floor not in self.destination_queue:
            self.destination_queue.append(call_floor)
        if destination_floor and destination_floor not in self.destination_queue:
            self.destination_queue.append(destination_floor)
        
        self.is_resting = False
        self.resting_since = None
    
    def step(self):
        if not self.destination_queue:
            return False
        
        next_floor = self.destination_queue[0]
        
        if self.current_floor < next_floor:
            self.direction = 'up'
            self.current_floor += 1
        elif self.current_floor > next_floor:
            self.direction = 'down'
            self.current_floor -= 1
        else:
            # Arrived at destination
            self.destination_queue.pop(0)
            # Stop here for one step to simulate arrival
            if not self.destination_queue:
                # No more destinations, start resting
                self.start_resting(datetime.now())
            # Always return False when arriving at a destination
            # This simulates the elevator stopping to pick up/drop of passengers
            return False
        
        return True

    def reset(self):
        """Reset the elevator to its initial state"""
        self.current_floor = 1
        self.direction = 'idle'
        self.is_resting = True
        self.resting_since = datetime.now()
        self.destination_queue = []

elevator = Elevator()


@app.route('/call', methods=['POST'])
def call_elevator():
    data = request.get_json()
    
    if not data or 'floor' not in data:
        return jsonify({'error': 'Floor is required'}), 400
    
    call_floor = data['floor']
    destination_floor = data.get('destination_floor')
    
    elevator.receive_call(call_floor, destination_floor)
    
    return jsonify({
        'message': 'Call received',
        'call_floor': call_floor,
        'destination_floor': destination_floor,
        'elevator_state': elevator.get_state()
    }), 201


@app.route('/step', methods=['POST'])
def step_simulation():
    moved = elevator.step()
    
    return jsonify({
        'message': 'Simulation stepped',
        'moved': moved,
        'elevator_state': elevator.get_state()
    })


@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        'elevator': elevator.get_state(),
        'total_logs': DemandLog.query.count()
    })


@app.route('/logs', methods=['GET'])
def get_logs():
    limit = request.args.get('limit', 100, type=int)
    logs = DemandLog.query.order_by(DemandLog.timestamp_called.desc()).limit(limit).all()
    
    return jsonify({
        'logs': [{
            'id': log.id,
            'timestamp_rested': log.timestamp_rested.isoformat(),
            'timestamp_called': log.timestamp_called.isoformat(),
            'resting_floor': log.resting_floor,
            'call_floor': log.call_floor,
            'destination_floor': log.destination_floor,
            'day_of_week': log.day_of_week,
            'hour_of_day': log.hour_of_day,
            'idle_time_seconds': (log.timestamp_called - log.timestamp_rested).total_seconds()
        } for log in logs]
    })


@app.route('/stats', methods=['GET'])
def get_stats():
    resting_patterns = db.session.query(
        DemandLog.resting_floor,
        DemandLog.call_floor,
        db.func.count(DemandLog.id).label('count')
    ).group_by(
        DemandLog.resting_floor,
        DemandLog.call_floor
    ).order_by(
        DemandLog.resting_floor,
        db.func.count(DemandLog.id).desc()
    ).all()
    
    return jsonify({
        'resting_patterns': [
            {
                'resting_floor': r.resting_floor,
                'call_floor': r.call_floor,
                'count': r.count
            } for r in resting_patterns
        ]
    })


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        elevator.start_resting(datetime.now())
    app.run(debug=True, host='0.0.0.0', port=5000) 