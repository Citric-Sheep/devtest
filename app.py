from flask import Flask
from models import db
from controllers import *

app = Flask(__name__)  # _name_ -> __name__
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elevator.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Routes  # Rotas -> Routes
@app.route('/api/elevator-demand', methods=['POST'])  # /api/demanda-elevador -> /api/elevator-demand
def route_register_elevator_demand():  # route_registrar_demanda_elevador -> route_register_elevator_demand
    return register_elevator_demand()

@app.route('/api/elevator-rest-floor', methods=['POST'])  # /api/andar-repouso-elevador -> /api/elevator-rest-floor
def route_register_elevator_rest_floor():  # route_registrar_andar_repouso_elevador -> route_register_elevator_rest_floor
    return register_elevator_rest_floor()

@app.route('/api/elevator-demands', methods=['GET'])  # /api/demandas-elevador -> /api/elevator-demands
def route_get_elevator_demands():  # route_get_demandas_elevador -> route_get_elevator_demands
    return get_elevator_demands()

@app.route('/api/elevator-demands/floor/<int:floor_id>', methods=['GET'])  # /api/demandas-elevador/andar/<int:andar_id> -> /api/elevator-demands/floor/<int:floor_id>
def route_get_elevator_demands_by_floor(floor_id):  # route_get_demandas_elevador_por_andar -> route_get_elevator_demands_by_floor
    return get_elevator_demands_by_floor(floor_id)

if __name__ == '__main__':  # _name_ -> __name__, _main_ -> '__main__'
    app.run(debug=True)
