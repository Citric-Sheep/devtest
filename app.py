from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elevator.db'
db = SQLAlchemy(app)


# Define the Floor model
class Floor(db.Model):
    floor_id = db.Column(db.Integer, primary_key=True)
    floor_number = db.Column(db.Integer, unique=True, nullable=False)


# Define the ElevatorEvent model
class ElevatorEvent(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    source_floor_id = db.Column(db.Integer, db.ForeignKey('floor.floor_id'), nullable=True)
    destination_floor_id = db.Column(db.Integer, db.ForeignKey('floor.floor_id'), nullable=True)
    num_persons = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    event_type = db.Column(db.String, nullable=False)


# Ensure that the tables are created within the app context
with app.app_context():
    db.create_all()


@app.route('/floors', methods=['POST'])
def add_floor():
    """
    Add a new floor to the database.
    """
    floor_number = request.json['floor_number']
    new_floor = Floor(floor_number=floor_number)
    db.session.add(new_floor)
    db.session.commit()
    return jsonify({'message': 'Floor added'}), 201


@app.route('/events', methods=['POST'])
def add_event():
    """
    Record a new elevator event.
    """
    source_floor_id = request.json.get('source_floor_id')
    destination_floor_id = request.json.get('destination_floor_id')
    num_persons = request.json.get('num_persons')
    weight = request.json.get('weight')
    event_type = request.json['event_type']

    new_event = ElevatorEvent(
        source_floor_id=source_floor_id,
        destination_floor_id=destination_floor_id,
        num_persons=num_persons,
        weight=weight,
        event_type=event_type
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'message': 'Event recorded'}), 201


@app.route('/events', methods=['GET'])
def get_events():
    """
    Retrieve all recorded elevator events.
    """
    events = ElevatorEvent.query.all()
    return jsonify([
        {
            'event_id': e.event_id,
            'timestamp': e.timestamp,
            'source_floor_id': e.source_floor_id,
            'destination_floor_id': e.destination_floor_id,
            'num_persons': e.num_persons,
            'weight': e.weight,
            'event_type': e.event_type
        } for e in events
    ])


if __name__ == '__main__':
    app.run(debug=True)
