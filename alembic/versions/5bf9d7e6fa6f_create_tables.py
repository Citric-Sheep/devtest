from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
from enum import Enum as PyEnum

class DemandStatusEnum(str, PyEnum):
    PENDING = "pending"
    COMPLETED = "completed"

class ElevatorStatusEnum(str, PyEnum):
    VACANT = "vacant"
    OCCUPIED = "occupied"

def upgrade():
    op.create_table(
        "elevators",
        Column("id", Integer, primary_key=True, index=True),
        Column("current_floor", Integer, nullable=False),
        Column("resting_floor", Integer, nullable=False),
        Column(
            "status",
            Enum(ElevatorStatusEnum, name="elevator_status"),
            default=ElevatorStatusEnum.VACANT,
            nullable=False,
            index=True,
        ),
    )

    op.create_table(
        "floors",
        Column("id", Integer, primary_key=True, index=True),
        Column("name", String(255), nullable=False),
    )

    op.create_table(
        "demands",
        Column("id", Integer, primary_key=True, index=True),
        Column("from_floor", Integer, nullable=False),
        Column("to_floor", Integer, nullable=False),
        Column("created_at", DateTime, nullable=False, server_default=sa.func.now()),
        Column(
            "status",
            Enum(DemandStatusEnum, name="demand_status"),
            default=DemandStatusEnum.COMPLETED,
            nullable=False,
            index=True,
        ),
    )

def downgrade():
    op.drop_table("demands")
    op.drop_table("floors")
    op.drop_table("elevators")