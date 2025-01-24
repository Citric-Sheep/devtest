from flask import Flask, request, jsonify
import service

app = Flask(__name__)

@app.route("/log_demand", methods=["POST"])
def log_demand():
    try:
        # Get data from the request
        data = request.get_json()
        demand_floor = data["demand_floor"]
        direction = data["direction"]
        
        # Log the demand using the service layer
        service.log_demand(demand_floor, direction)
        
        return jsonify({"message": "Demand logged successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/get_feature_data", methods=["GET"])
def get_feature_data():
    try:
        # Get the feature data (joined table data)
        feature_data = service.get_feature_data()
        return jsonify({"data": feature_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
