##############
# Libraries #
##############

from sqlalchemy.sql import func

from database.db_models import CatalogElevatorStates, CatalogOrderCategories, CatalogOrderTypes, CatalogOrderMovements, CatalogOrderStatus, Elevators

#######################
# Catalog input data #
#######################

catalog_data = {
    CatalogElevatorStates: [
        {'code': 0, 'description': 'UNMATCHED STATE', 'state': True, 'created_on': func.now()},
        {'code': 1, 'description': 'ACTIVE', 'state': True, 'created_on': func.now()},
        {'code': 2, 'description': 'INACTIVE', 'state': True, 'created_on': func.now()},
        {'code': 3, 'description': 'MAINTENANCE', 'state': True, 'created_on': func.now()}
    ],
    CatalogOrderCategories: [
        {'code': 0, 'description': 'UNMATCHED CATEGORY', 'state': True, 'created_on': func.now()},
        {'code': 1, 'description': 'ELEVATOR DEMAND', 'state': True, 'created_on': func.now()},
        {'code': 2, 'description': 'FLOOR DEMAND', 'state': True, 'created_on': func.now()}
    ],
    CatalogOrderTypes: [
        {'code': 0, 'description': 'UNMATCHED DEMAND TYPE', 'state': True, 'created_on': func.now()},
        {'code': 1, 'description': 'UP', 'state': True, 'created_on': func.now()},
        {'code': 2, 'description': 'DOWN', 'state': True, 'created_on': func.now()},
    ],
    CatalogOrderMovements: [
        {'code': 0, 'description': 'UNMATCHED MOVEMENT', 'state': True, 'created_on': func.now()},
        {'code': 1, 'description': 'UP', 'state': True, 'created_on': func.now()},
        {'code': 2, 'description': 'DOWN', 'state': True, 'created_on': func.now()},
        {'code': 3, 'description': 'REST', 'state': True, 'created_on': func.now()}
    ],
    CatalogOrderStatus: [
        {'code': 0, 'description': 'UNMATCHED REQUEST STATUS', 'state': True, 'created_on': func.now()},
        {'code': 1, 'description': 'IN PROCESS', 'state': True, 'created_on': func.now()},
        {'code': 2, 'description': 'COMPLETED', 'state': True, 'created_on': func.now()},
    ],
    Elevators: [
        {'elevators_name': 'ELEVATOR TOWER 1', 'elevators_floors': 10, 'elevators_rooms': 6, 'elevators_state': 1, 'elevators_created_on': func.now()},
        {'elevators_name': 'ELEVATOR TOWER 2', 'elevators_floors': 12, 'elevators_rooms': 6, 'elevators_state': 1, 'elevators_created_on': func.now()},
        {'elevators_name': 'ELEVATOR TOWER 3', 'elevators_floors': 10, 'elevators_rooms': 4, 'elevators_state': 2, 'elevators_created_on': func.now()}
    ]
}
