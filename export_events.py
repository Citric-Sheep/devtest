import csv
from sqlalchemy.orm import Session
from app.models import ElevatorEvent
from app.database import SessionLocal

def export_events_to_csv(filename="events_export.csv"):
    db: Session = SessionLocal()
    events = db.query(ElevatorEvent).all()
    db.close()

    with open(filename, mode='w', newline='') as csv_file:
        fieldnames = ['id', 'elevator_id', 'event_type', 'from_floor', 'to_floor', 'timestamp']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for event in events:
            writer.writerow({
                'id': event.id,
                'elevator_id': event.elevator_id,
                'event_type': event.event_type,
                'from_floor': event.from_floor,
                'to_floor': event.to_floor,
                'timestamp': event.timestamp
            })

if __name__ == "__main__":
    export_events_to_csv()
