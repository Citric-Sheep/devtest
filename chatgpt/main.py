from flask import Flask, Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, Elevator, ElevatorDemand, ElevatorState
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elevator.db'
db.init_app(app)

@app.route('/elevator', methods=['POST'])
def create_elevator():
    data = request.get_json()
    elevator = Elevator(name=data['name'])
    db.session.add(elevator)
    db.session.commit()
    return jsonify({'message': 'Elevator created', 'elevator_id': elevator.id}), 201

@app.route('/demand', methods=['POST'])
def create_demand():
    data = request.get_json()
    new_demand = ElevatorDemand(floor=data['floor'],elevator_id=data['elevator_id'])
    db.session.add(new_demand)
    db.session.commit()
    return jsonify({'message': 'Demand created'}), 201


@app.route('/state', methods=['POST'])
def create_state():
    data = request.get_json()
    new_state = ElevatorState(
        floor=data['floor'], 
        vacant=data['vacant'],
        elevator_id=data['elevator_id']
        )
    db.session.add(new_state)
    db.session.commit()
    return jsonify({'message': 'State created'}), 201


@app.route('/dataset', methods=['GET'])
def generate_dataset():
    date_str = request.args.get('date')  # YYYY-MM-DD
    enddate_str  = request.args.get('enddate')  # YYYY-MM-DD
    holiday_param = request.args.get('holiday', 'false').lower()
    if not date_str:
        return jsonify({'error': 'You must provide a date in format YYYY-MM-DD'}), 400

    try:
        date = pd.to_datetime(date_str)
    except:
        return jsonify({'error': 'Invalid date format'}), 400

    start = pd.Timestamp(date.date())
    if enddate_str:
        try:
            # end = pd.to_datetime(enddate_str)
            end = pd.to_datetime(enddate_str) + pd.Timedelta(days=1)
        except:
            return jsonify({'error': 'Invalid end date format'}), 400
    else:
        end = start + pd.Timedelta(days=1)
    is_holiday = holiday_param in ['true', '1', 'yes']

    demands = ElevatorDemand.query.filter(
        ElevatorDemand.timestamp >= start,
        ElevatorDemand.timestamp < end
    ).all()

    data = [{
        'timestamp': d.timestamp,
        'floor': d.floor
    } for d in demands]

    df = pd.DataFrame(data)

    if df.empty:
        return jsonify([])

    # features
    df['hour'] = df['timestamp'].dt.hour
    df['minute'] = df['timestamp'].dt.minute
    df['weekday'] = df['timestamp'].dt.weekday
    df['month'] = df['timestamp'].dt.month
    df['is_holiday'] = is_holiday
    df['is_weekend'] = df['weekday'].isin([5, 6])

    df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S')

    return jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
