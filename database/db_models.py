##############
# Libraries #
##############

from sqlalchemy import Boolean, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from sqlalchemy.sql import func


####################
# Database models #
####################

class BaseModel(DeclarativeBase):
    pass


class Elevators(BaseModel):
    __tablename__ = "elevators"
    elevator_id = mapped_column(Integer,
                                primary_key=True,
                                unique=True,
                                nullable=False)
    elevators_name = mapped_column(String(255),
                                   nullable=False)
    elevators_details = mapped_column(String,
                                      nullable=True)
    elevators_floors = mapped_column(Integer,
                                     nullable=False)
    elevators_rooms = mapped_column(Integer,
                                    nullable=False)
    elevators_state = mapped_column(ForeignKey("catalog_elevator_states.code"),
                                    nullable=False)
    elevators_request_status = mapped_column(ForeignKey("catalog_order_status.code"), nullable=True)
    elevators_request_queue = mapped_column(String, nullable=True)

    elevators_created_on = mapped_column(DateTime(timezone=True),
                                         server_default=func.now(),
                                         nullable=False)
    elevators_update_on = mapped_column(DateTime(timezone=True),
                                        onupdate=func.now(),
                                        nullable=True)

    elevators_elevator_orders: Mapped["ElevatorOrders"] = relationship(back_populates="elevator_orders_elevators",
                                                                       cascade="all,delete-orphan")
    elevators_elevator_status: Mapped["ElevatorStatus"] = relationship(back_populates="elevator_status_elevators",
                                                                       cascade="all,delete-orphan")


class ElevatorOrders(BaseModel):
    __tablename__ = "elevator_orders"
    elevator_order_id = mapped_column(Integer,
                                      primary_key=True,
                                      unique=True,
                                      nullable=False)
    elevator_id = mapped_column(ForeignKey("elevators.elevator_id",
                                ondelete="SET NULL"),
                                nullable=True)
    elevator_order_demand_category = mapped_column(ForeignKey("catalog_order_categories.code"),
                                                   nullable=False)
    elevator_order_demand_type = mapped_column(ForeignKey("catalog_order_types.code"),
                                               nullable=True)
    elevator_order_demand_floor = mapped_column(Integer,
                                                nullable=True)
    elevator_order_current_floor = mapped_column(Integer,
                                                 nullable=False)
    elevator_order_movement_status = mapped_column(ForeignKey("catalog_order_movements.code"),
                                                   nullable=False)
    elevator_order_created_on = mapped_column(DateTime(timezone=True),
                                              server_default=func.now(),
                                              nullable=False)
    elevator_order_update_on = mapped_column(DateTime(timezone=True),
                                             onupdate=func.now(),
                                             nullable=True)

    elevator_orders_elevators: Mapped["Elevators"] = relationship(back_populates="elevators_elevator_orders")
    elevator_orders_catalog_order_categories: Mapped["CatalogOrderCategories"] = relationship()
    elevator_orders_catalog_order_types: Mapped["CatalogOrderTypes"] = relationship()
    elevator_orders_catalog_order_movements: Mapped["CatalogOrderMovements"] = relationship()


class ElevatorStatus(BaseModel):
    __tablename__ = "elevator_status"
    elevator_status_id = mapped_column(Integer,
                                       primary_key=True,
                                       unique=True,
                                       nullable=False)
    elevator_id = mapped_column(ForeignKey("elevators.elevator_id",
                                           ondelete="SET NULL"),
                                nullable=True)
    elevator_status_movement = mapped_column(ForeignKey("catalog_order_movements.code"),
                                             nullable=False)
    elevator_status_current_floor = mapped_column(Integer,
                                                  nullable=False)
    elevator_status_final_floor = mapped_column(Integer,
                                                nullable=True)
    elevator_status_created_on = mapped_column(DateTime(timezone=True),
                                               server_default=func.now(),
                                               nullable=False)

    elevator_status_elevators: Mapped["Elevators"] = relationship(back_populates="elevators_elevator_status")
    elevator_status_catalog_order_movements: Mapped["CatalogOrderMovements"] = relationship()


class CatalogElevatorStates(BaseModel):
    __tablename__ = "catalog_elevator_states"
    id = mapped_column(Integer,
                       primary_key=True,
                       unique=True,
                       nullable=False)
    code = mapped_column(Integer,
                         unique=True,
                         nullable=False)
    description = mapped_column(String(255),
                                nullable=False)
    state = mapped_column(Boolean,
                          nullable=False)
    created_on = mapped_column(DateTime(timezone=True),
                               server_default=func.now(),
                               nullable=False)
    updated_on = mapped_column(DateTime(timezone=True),
                               onupdate=func.now(),
                               nullable=True)


class CatalogOrderCategories(BaseModel):
    __tablename__ = "catalog_order_categories"
    id = mapped_column(Integer,
                       primary_key=True,
                       unique=True,
                       nullable=False)
    code = mapped_column(Integer,
                         unique=True,
                         nullable=False)
    description = mapped_column(String(255),
                                nullable=False)
    state = mapped_column(Boolean,
                          nullable=False)
    created_on = mapped_column(DateTime(timezone=True),
                               server_default=func.now(),
                               nullable=False)
    updated_on = mapped_column(DateTime(timezone=True),
                               onupdate=func.now(),
                               nullable=True)


class CatalogOrderTypes(BaseModel):
    __tablename__ = "catalog_order_types"
    id = mapped_column(Integer,
                       primary_key=True,
                       unique=True,
                       nullable=False)
    code = mapped_column(Integer,
                         unique=True,
                         nullable=False)
    description = mapped_column(String(255),
                                nullable=False)
    state = mapped_column(Boolean,
                          nullable=False)
    created_on = mapped_column(DateTime(timezone=True),
                               server_default=func.now(),
                               nullable=False)
    updated_on = mapped_column(DateTime(timezone=True),
                               onupdate=func.now(),
                               nullable=True)


class CatalogOrderMovements(BaseModel):
    __tablename__ = "catalog_order_movements"
    id = mapped_column(Integer,
                       primary_key=True,
                       unique=True,
                       nullable=False)
    code = mapped_column(Integer,
                         unique=True,
                         nullable=False)
    description = mapped_column(String(255),
                                nullable=False)
    state = mapped_column(Boolean,
                          nullable=False)
    created_on = mapped_column(DateTime(timezone=True),
                               server_default=func.now(),
                               nullable=False)
    updated_on = mapped_column(DateTime(timezone=True),
                               onupdate=func.now(),
                               nullable=True)


class CatalogOrderStatus(BaseModel):
    __tablename__ = "catalog_order_status"
    id = mapped_column(Integer,
                       primary_key=True,
                       unique=True,
                       nullable=False)
    code = mapped_column(Integer,
                         unique=True,
                         nullable=False)
    description = mapped_column(String(255),
                                nullable=False)
    state = mapped_column(Boolean,
                          nullable=False)
    created_on = mapped_column(DateTime(timezone=True),
                               server_default=func.now(),
                               nullable=False)
    updated_on = mapped_column(DateTime(timezone=True),
                               onupdate=func.now(),
                               nullable=True)
