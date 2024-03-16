from flask import Flask
from database import init_app, db
from dotenv import load_dotenv
import os
from routes import demand_blueprint, elevator_blueprint, predictor_blueprint

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

# Inicializa la aplicación y las migraciones
init_app(app)

app.register_blueprint(demand_blueprint)
app.register_blueprint(elevator_blueprint)
app.register_blueprint(predictor_blueprint)

# Registra los modelos
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
