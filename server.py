import commons
from sanic import Sanic

from src.entrypoints.elevator_controller import elevator_bp

app = Sanic("ElevatorApi")
commons.app = app
app.blueprint(elevator_bp)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        access_log=True,
        auto_reload=True,
    )
