from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


# ---------------- Models ---------------- #
class Elevator(db.Model):
    __tablename__ = "elevator"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    capacity = db.Column(db.Integer, default=8)
    is_operational = db.Column(db.Boolean, default=True)
    current_floor = db.Column(db.Integer, default=1)


class ElevatorRequest(db.Model):
    __tablename__ = "elevator_request"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    elevator_id = db.Column(db.Integer, db.ForeignKey("elevator.id"))
    floor = db.Column(db.Integer, nullable=False)
    direction = db.Column(db.String(5), default=None)  # 'up' or 'down'
    request_type = db.Column(db.String(10))  # 'internal' or 'external'
    request_status = db.Column(
        db.String(15), default="pending"
    )  # 'pending', 'in_progress', etc.


class ScheduledJob(db.Model):
    __tablename__ = "scheduled_job"
    id = db.Column(db.Integer, primary_key=True)
    elevator_id = db.Column(
        db.Integer, db.ForeignKey("elevator.id"), nullable=False
    )
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow
    )  # creation time
    scheduled_time = db.Column(db.DateTime)  # planned execution time
    completion_time = db.Column(db.DateTime)
    floor_arrival = db.Column(db.Integer)
    floor_destination = db.Column(db.Integer)
    previous_job_id = db.Column(
        db.Integer, db.ForeignKey("scheduled_job.id"), default=None
    )
    next_job_id = db.Column(
        db.Integer, db.ForeignKey("scheduled_job.id"), default=None
    )
    call_status = db.Column(db.String(15), default="pending")


class JobRequestLink(db.Model):
    __tablename__ = "job_request_link"
    job_id = db.Column(
        db.Integer, db.ForeignKey("scheduled_job.id"), primary_key=True
    )
    request_id = db.Column(
        db.Integer, db.ForeignKey("elevator_request.id"), primary_key=True
    )


class ElevatorDailyMetrics(db.Model):
    __tablename__ = "elevator_daily_metrics"
    elevator_id = db.Column(
        db.Integer, db.ForeignKey("elevator.id"), primary_key=True
    )
    capacity = db.Column(db.Integer)
    is_operational = db.Column(db.Boolean, default=True)
    total_trips = db.Column(db.Integer, default=0)
    total_distance = db.Column(db.Integer, default=0)
    max_weight_occupancy = db.Column(db.Integer)
    energy_consumption = db.Column(db.Float, default=0.0)
    time_idle = db.Column(db.Integer, default=0)
    time_moving = db.Column(db.Integer, default=0)


class Floors(db.Model):
    __tablename__ = "floors"
    floor_id = db.Column(db.Integer, primary_key=True)
    floor_number = db.Column(db.Integer, unique=True)
    is_accessible = db.Column(db.Boolean, default=True)


# --------------- Helper Functions ------------ #


def validate_previous_job_sequence(previous_job_id, scheduled_time):
    """Example business rule:
    Ensures scheduled_time is after the previous job's scheduled_time.
    """
    if not previous_job_id or not scheduled_time:
        return True  # no constraint needed
    prev_job = db.session.get(ScheduledJob, previous_job_id)
    if not prev_job:
        return True
    if prev_job.scheduled_time and scheduled_time < prev_job.scheduled_time:
        return False
    return True


def is_elevator_operational(elevator_id):
    elevator = db.session.get(Elevator, elevator_id)
    return elevator.is_operational if elevator else False


# --------------- Elevator Endpoints (CRUD) --------------- #
def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    db.init_app(app)

    @app.route("/elevators", methods=["POST"])
    def create_elevator():
        data = request.get_json()
        # Example JSON:
        # {
        #   "name": "Elevator A",
        #   "capacity": 8,
        #   "is_operational": true,
        #   "current_floor": 1
        # }
        new_elevator = Elevator(
            name=data["name"],
            capacity=data.get("capacity", 8),
            is_operational=data.get("is_operational", True),
            current_floor=data.get("current_floor", 1),
        )
        db.session.add(new_elevator)
        db.session.commit()
        return (
            jsonify(
                {"message": "Elevator created", "elevator_id": new_elevator.id}
            ),
            201,
        )

    @app.route("/elevators/<int:elevator_id>", methods=["GET"])
    def get_elevator(elevator_id):
        elevator = Elevator.query.get_or_404(elevator_id)
        return (
            jsonify(
                {
                    "id": elevator.id,
                    "name": elevator.name,
                    "capacity": elevator.capacity,
                    "is_operational": elevator.is_operational,
                    "current_floor": elevator.current_floor,
                }
            ),
            200,
        )

    @app.route("/elevators/<int:elevator_id>", methods=["PUT"])
    def update_elevator(elevator_id):
        elevator = Elevator.query.get_or_404(elevator_id)
        data = request.get_json()
        elevator.name = data.get("name", elevator.name)
        elevator.capacity = data.get("capacity", elevator.capacity)
        elevator.is_operational = data.get(
            "is_operational", elevator.is_operational
        )
        elevator.current_floor = data.get(
            "current_floor", elevator.current_floor
        )
        db.session.commit()
        return jsonify({"message": "Elevator updated"}), 200

    @app.route("/elevators/<int:elevator_id>", methods=["DELETE"])
    def delete_elevator(elevator_id):
        elevator = Elevator.query.get_or_404(elevator_id)
        db.session.delete(elevator)
        db.session.commit()
        return jsonify({"message": "Elevator deleted"}), 200

    # --------------- Elevator Requests Endpoints (CRUD) --------------- #
    @app.route("/requests", methods=["POST"])
    def create_request():
        """
        Example JSON body:
        {
        "elevator_id": 1,
        "floor": 5,
        "direction": "up",
        "request_type": "external"
        }
        """
        data = request.get_json()
        new_request = ElevatorRequest(
            elevator_id=data.get("elevator_id"),
            floor=data["floor"],
            direction=data.get("direction"),
            request_type=data.get("request_type", "external"),
        )
        db.session.add(new_request)
        db.session.commit()
        return (
            jsonify(
                {"message": "Request created", "request_id": new_request.id}
            ),
            201,
        )

    @app.route("/requests/<int:request_id>", methods=["GET"])
    def get_request(request_id):
        req = ElevatorRequest.query.get_or_404(request_id)
        return (
            jsonify(
                {
                    "id": req.id,
                    "timestamp": req.timestamp.isoformat(),
                    "elevator_id": req.elevator_id,
                    "floor": req.floor,
                    "direction": req.direction,
                    "request_type": req.request_type,
                    "request_status": req.request_status,
                }
            ),
            200,
        )

    @app.route("/requests/<int:request_id>", methods=["PUT"])
    def update_request(request_id):
        req = ElevatorRequest.query.get_or_404(request_id)
        data = request.get_json()
        req.elevator_id = data.get("elevator_id", req.elevator_id)
        req.floor = data.get("floor", req.floor)
        req.direction = data.get("direction", req.direction)
        req.request_type = data.get("request_type", req.request_type)
        req.request_status = data.get("request_status", req.request_status)
        db.session.commit()
        return jsonify({"message": "Request updated"}), 200

    @app.route("/requests/<int:request_id>", methods=["DELETE"])
    def delete_request(request_id):
        req = ElevatorRequest.query.get_or_404(request_id)
        db.session.delete(req)
        db.session.commit()
        return jsonify({"message": "Request deleted"}), 200

    # --------------- Scheduled Jobs Endpoints (CRUD) --------------- #
    @app.route("/jobs", methods=["POST"])
    def create_job():
        """
        Example JSON body:
        {
        "elevator_id": 1,
        "scheduled_time": "2025-01-22T10:00:00",
        "floor_arrival": 2,
        "floor_destination": 8,
        "previous_job_id": 3,
        "requests": [1, 2]  -- request IDs to link
        }
        """
        data = request.get_json()

        # 1) Check if elevator is operational
        if not is_elevator_operational(data["elevator_id"]):
            return jsonify({"error": "Elevator is not operational"}), 400

        # 2) Validate job sequence
        scheduled_time = None
        if data.get("scheduled_time"):
            scheduled_time = datetime.fromisoformat(data["scheduled_time"])
        if not validate_previous_job_sequence(
            data.get("previous_job_id"), scheduled_time
        ):
            return (
                jsonify({"error": "Invalid scheduling time by previous job"}),
                400,
            )

        new_job = ScheduledJob(
            elevator_id=data["elevator_id"],
            scheduled_time=scheduled_time,
            floor_arrival=data.get("floor_arrival"),
            floor_destination=data.get("floor_destination"),
            previous_job_id=data.get("previous_job_id"),
            next_job_id=data.get("next_job_id"),
            call_status=data.get("call_status", "pending"),
        )
        db.session.add(new_job)
        db.session.flush()  # so new_job.id is available

        # Link any request IDs to this job
        request_ids = data.get("requests", [])
        for req_id in request_ids:
            # optionally check that the request exists or is pending
            link = JobRequestLink(job_id=new_job.id, request_id=req_id)
            db.session.add(link)

        db.session.commit()
        return (
            jsonify(
                {"message": "Scheduled job created", "job_id": new_job.id}
            ),
            201,
        )

    @app.route("/jobs/<int:job_id>", methods=["GET"])
    def get_job(job_id):
        job = ScheduledJob.query.get_or_404(job_id)
        # gather linked requests
        linked_requests = (
            db.session.query(JobRequestLink).filter_by(job_id=job_id).all()
        )
        request_ids = [lr.request_id for lr in linked_requests]
        return (
            jsonify(
                {
                    "id": job.id,
                    "elevator_id": job.elevator_id,
                    "timestamp": job.timestamp.isoformat(),
                    "scheduled_time": (
                        job.scheduled_time.isoformat()
                        if job.scheduled_time
                        else None
                    ),
                    "completion_time": (
                        job.completion_time.isoformat()
                        if job.completion_time
                        else None
                    ),
                    "floor_arrival": job.floor_arrival,
                    "floor_destination": job.floor_destination,
                    "previous_job_id": job.previous_job_id,
                    "next_job_id": job.next_job_id,
                    "call_status": job.call_status,
                    "requests": request_ids,
                }
            ),
            200,
        )

    @app.route("/jobs/<int:job_id>", methods=["PUT"])
    def update_job(job_id):
        job = ScheduledJob.query.get_or_404(job_id)
        data = request.get_json()

        # Example: Check capacity or elevator operational
        # changes if elevator_id changes
        if "elevator_id" in data:
            if not is_elevator_operational(data["elevator_id"]):
                return (
                    jsonify({"error": "Target elevator is not operational"}),
                    400,
                )
            job.elevator_id = data["elevator_id"]

        # scheduled_time, completion_time
        if "scheduled_time" in data:
            new_time = datetime.fromisoformat(data["scheduled_time"])
            # re-validate job sequence if there's a previous job
            if not validate_previous_job_sequence(
                job.previous_job_id, new_time
            ):
                return (
                    jsonify(
                        {"error": "Invalid scheduling time by previous job"}
                    ),
                    400,
                )
            job.scheduled_time = new_time

        if "completion_time" in data:
            job.completion_time = datetime.fromisoformat(
                data["completion_time"]
            )

        job.floor_arrival = data.get("floor_arrival", job.floor_arrival)
        job.floor_destination = data.get(
            "floor_destination", job.floor_destination
        )
        job.call_status = data.get("call_status", job.call_status)

        db.session.commit()
        return jsonify({"message": "Job updated"}), 200

    @app.route("/jobs/<int:job_id>", methods=["DELETE"])
    def delete_job(job_id):
        job = ScheduledJob.query.get_or_404(job_id)
        # optionally handle link cleanup or handle ON DELETE CASCADE
        # (SQLite doesn't support ON DELETE CASCADE by default without PRAGMA)
        JobRequestLink.query.filter_by(job_id=job.id).delete()
        db.session.delete(job)
        db.session.commit()
        return jsonify({"message": "Job deleted"}), 200

    return app


# --------------- Initialize DB --------------- #
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
