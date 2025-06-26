# Import necessary libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import text

# Set up Flask app and connect to SQLite database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elevator.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Turn off warnings for SQLAlchemy
db = SQLAlchemy(app)


# Class model for elevator demands
class ElevatorDemand(db.Model):
    __tablename__ = 'elevator_demands'  # Set table name and ForeignKey reference
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now())  # Store when the demand was made
    floor = db.Column(db.Integer, nullable=False)  # Floor number, can be positive or negative
    day_of_week = db.Column(db.Integer, nullable=False)  # Day of the week (0-6, Mon-Sun)
    hour_of_day = db.Column(db.Integer, nullable=False)  # Hour of the day (0-23)

    def __init__(self, floor):
        self.floor = floor
        self.day_of_week = datetime.now().weekday()  # Save the current day of the week
        self.hour_of_day = datetime.now().hour  # Save the current hour

    # Convert demand to a dictionary for JSON response
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'floor': self.floor,
            'day_of_week': self.day_of_week,
            'hour_of_day': self.hour_of_day
        }


# Class model for elevator states
class ElevatorState(db.Model):
    __tablename__ = 'elevator_states'  # Set table name
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now())  # Store when the state was recorded
    floor = db.Column(db.Integer, nullable=False)  # Current floor of the elevator
    vacant = db.Column(db.Boolean, nullable=False)  # True if elevator is empty, False if not
    day_of_week = db.Column(db.Integer, nullable=False)  # Day of the week (0-6)
    hour_of_day = db.Column(db.Integer, nullable=False)  # Hour of the day (0-23)
    # Link to a demand if the elevator is not vacant
    demand_id = db.Column(db.Integer, db.ForeignKey('elevator_demands.id'), nullable=True)
    # Set up relationship to access demand data easily
    demand = db.relationship('ElevatorDemand', backref=db.backref('states', lazy=True))

    def __init__(self, floor, vacant, demand_id=None):
        self.floor = floor
        self.vacant = vacant
        self.demand_id = demand_id
        self.day_of_week = datetime.now().weekday()  # Save current day
        self.hour_of_day = datetime.now().hour  # Save current hour

    # Convert state to a dictionary for JSON response
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'floor': self.floor,
            'vacant': self.vacant,
            'day_of_week': self.day_of_week,
            'hour_of_day': self.hour_of_day,
            'demand_id': self.demand_id
        }


# Create a demand when someone calls the elevator
@app.route('/demand', methods=['POST'])
def create_demand():
    data = request.get_json()
    if not isinstance(data.get('floor'), int):
        return jsonify({'error': 'Floor must be an integer'}), 400  # Check if floor is valid
    new_demand = ElevatorDemand(floor=data['floor'])  # Create new demand
    db.session.add(new_demand)  # Add to database
    db.session.commit()  # Save changes
    # Return the created demand with its details
    return jsonify({'message': 'Demand created', 'demand': new_demand.to_dict()}), 201


# Get a specific demand by ID
@app.route('/demand/<int:id>', methods=['GET'])
def get_demand(id):
    demand = ElevatorDemand.query.get_or_404(id)  # Find demand or return 404
    return jsonify(demand.to_dict()), 200  # Return demand details


# Get all demands
@app.route('/demands', methods=['GET'])
def get_all_demands():
    demands = ElevatorDemand.query.all()  # Grab all demands from the database
    return jsonify([demand.to_dict() for demand in demands]), 200  # Return list of demands


# Update an existing demand
@app.route('/demand/<int:id>', methods=['PUT'])
def update_demand(id):
    demand = ElevatorDemand.query.get_or_404(id)  # Find demand or 404
    data = request.get_json()
    if not isinstance(data.get('floor'), int):
        return jsonify({'error': 'Floor must be an integer'}), 400  # Validate floor
    demand.floor = data['floor']  # Update floor
    db.session.commit()  # Save changes
    return jsonify({'message': 'Demand updated', 'demand': demand.to_dict()}), 200  # Return updated demand


# Delete a demand
@app.route('/demand/<int:id>', methods=['DELETE'])
def delete_demand(id):
    demand = ElevatorDemand.query.get_or_404(id)  # Find demand or 404
    db.session.delete(demand)  # Remove it
    db.session.commit()  # Save changes
    return jsonify({'message': 'Demand deleted'}), 200  # Confirm deletion


# Create a new elevator state
@app.route('/state', methods=['POST'])
def create_state():
    data = request.get_json()
    if not isinstance(data.get('floor'), int):
        return jsonify({'error': 'Floor must be an integer'}), 400  # Check floor is an integer
    if not isinstance(data.get('vacant'), bool):
        return jsonify({'error': 'Vacant must be a boolean'}), 400  # Check vacant is boolean
    demand_id = data.get('demand_id')
    if not data['vacant'] and demand_id is None:
        return jsonify({'error': 'Non-vacant state requires a valid demand_id'}), 400  # Check non-vacant states
    if demand_id is not None and ElevatorDemand.query.get(demand_id) is None:
        return jsonify({'error': 'Invalid demand_id'}), 400  # Validate demand_id
    new_state = ElevatorState(floor=data['floor'], vacant=data['vacant'], demand_id=demand_id)  # Create new state
    db.session.add(new_state)  # Add to database
    db.session.commit()  # Save changes
    return jsonify({'message': 'State created', 'state': new_state.to_dict()}), 201  # Return created state


# Get a specific state by its ID
@app.route('/state/<int:id>', methods=['GET'])
def get_state(id):
    state = ElevatorState.query.get_or_404(id)  # Find state or 404
    return jsonify(state.to_dict()), 200  # Return state details


# Get all states
@app.route('/states', methods=['GET'])
def get_all_states():
    states = ElevatorState.query.all()  # Grab all states
    return jsonify([state.to_dict() for state in states]), 200  # Return list of states


# Update an existing state
@app.route('/state/<int:id>', methods=['PUT'])
def update_state(id):
    state = ElevatorState.query.get_or_404(id)  # Find state or 404
    data = request.get_json()
    if not isinstance(data.get('floor'), int):
        return jsonify({'error': 'Floor must be an integer'}), 400  # Validate floor
    if not isinstance(data.get('vacant'), bool):
        return jsonify({'error': 'Vacant must be a boolean'}), 400  # Validate vacant
    demand_id = data.get('demand_id')
    if not data['vacant'] and demand_id is None:
        return jsonify({'error': 'Non-vacant state requires a valid demand_id'}), 400  # Check non-vacant states
    if demand_id is not None and ElevatorDemand.query.get(demand_id) is None:
        return jsonify({'error': 'Invalid demand_id'}), 400  # Validate demand_id
    state.floor = data['floor']  # Update floor
    state.vacant = data['vacant']  # Update vacant status
    state.demand_id = demand_id  # Update demand_id
    db.session.commit()  # Save changes
    return jsonify({'message': 'State updated', 'state': state.to_dict()}), 200  # Return updated state


# Delete a state
@app.route('/state/<int:id>', methods=['DELETE'])
def delete_state(id):
    state = ElevatorState.query.get_or_404(id)  # Find state or 404
    db.session.delete(state)  # Remove it
    db.session.commit()  # Save changes
    return jsonify({'message': 'State deleted'}), 200  # Confirm deletion


# Start the app and create database tables
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Set up the database tables
        with db.engine.connect() as connection:
            connection.execute(text('CREATE INDEX IF NOT EXISTS idx_demands_timestamp ON elevator_demands(timestamp)'))
            connection.execute(text('CREATE INDEX IF NOT EXISTS idx_states_timestamp ON elevator_states(timestamp)'))
            connection.execute(text('CREATE INDEX IF NOT EXISTS idx_demands_floor ON elevator_demands(floor)'))
            connection.execute(text('CREATE INDEX IF NOT EXISTS idx_states_floor ON elevator_states(floor)'))
        print("Database tables created!")
    app.run(debug=True)  # Run the app in debug mode
