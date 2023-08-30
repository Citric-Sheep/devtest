# Documentation for the Citric Sheep Application

---

## Libraries

- **logging**: The built-in Python library used for logging application events.
- **FastAPI**: A modern, fast web framework for building APIs with Python 3.7+. 
- **configure_project_attributes**: This module from our configuration folder contains details related to the project's attributes.
- **elevator_router**: From the `apps.elevator` package, this module is responsible for routes related to the elevator functionality of the application.
- **os**: Interact with the operating system. Used for getting paths, environment variables, etc.
- **dotenv**: A library to load environment variables from a `.env` file.
- **sqlalchemy**: The SQL Toolkit and Object-Relational Mapping (ORM) library for Python. We are importing functionalities to create an engine and manage sessions.
- **uvicorn**: A lightning-fast ASGI server implementation, using uvloop and httptools.
- **psycopg2**: A PostgreSQL database adapter for Python.
- **pydantic**: Data validation and settings management using Python type hinting.
- **pathlib**: A library for representing the file system path semantics of different operating systems.
- 

## Logger Configuration

The logger is configured to display logs at the `INFO` level. Each log will provide:
- The time the log event occurred.
- The severity level (INFO, WARNING, ERROR, etc.)
- The actual log message.

The format of each log is `"%Y-%m-%d %H:%M:%S - LEVEL - Message"`, where `LEVEL` is the severity level of the log.

## Load .env Files

A path to the `.env` file, located within the `configuration` directory, is constructed. The `load_dotenv` function is then used to load these environment variables, making them accessible via the `os.getenv` function throughout the application.

## Configuration of Project Attributes

The `ConfigurationProjectAttributes` class is defined to fetch and store essential project attributes:

- `PROJECT_NAME`: Represents the name of the project.
- `PROJECT_VERSION`: Represents the version of the project.

Both attributes fetch their values from environment variables.

## Configuration of Database Instances

Two classes are defined to fetch and store database credentials:

1. `ConfigurationDbCredentials`: This class fetches and stores the credentials for the primary database:
    - `DB_USER`: Database user.
    - `DB_PASSWORD`: Database password.
    - `DB_SERVER`: Server where the database is hosted, defaults to "localhost".
    - `DB_PORT`: Port on which the database listens, defaults to 5432.
    - `DB_NAME`: Name of the database, defaults to "tdd".

   A connection URL (`DB_URL`) is also constructed for PostgreSQL connections.

2. `ConfigurationTestDbCredentials`: Similar to the above but specifically for the test database.

## Execution of Configuration Attributes

Instances of the configuration classes are created to fetch and store the required attributes and configurations:

- `configure_project_attributes`: Holds project-related attributes.
- `configure_bd_credentials`: Holds primary database configurations.
- `configure_bd_test_credentials`: Holds test database configurations.

## APP Configuration

We create an instance of FastAPI, setting its `title` and `version` attributes using the values stored in the `configure_project_attributes` module. 

- `title`: Name of the project.
- `version`: Version of the project.

## APP Main Routers

The main application, `app_main`, incorporates the `elevator_router`. This means that the routes defined in `elevator_router` are registered with our main FastAPI application and are accessible once the application starts.

## Database Connection

- `db_sqlalchemy_url`: Fetches the database URL from the previously configured credentials.
  
- `db_sqlalchemy_engine`: Creates a SQLAlchemy engine using the database URL. This engine maintains a connection pool with a size of 20.
  
- `db_sqlalchemy_session`: Constructs a session factory bound to the engine. The session is set up with configurations to not autocommit transactions and not to autoflush operations automatically.

- `db_connection`: Returns a session instance from the session factory. This session is used to interact with the database.

## Database Models

- **BaseModel**: This is a declarative base class for all ORM models in the application.

- **Elevators**: Represents a table in the database to store information about different elevators.
  
- **ElevatorOrders**: Represents a table to store elevator requests or orders. It has relationships defined with the `Elevators` model and various catalog models.

- **ElevatorStatus**: Represents a table to store the current status of an elevator.

- **CatalogElevatorStates**: A catalog table to store different possible states an elevator can be in.

- **CatalogOrderCategories**: A catalog table to store different categories of elevator orders.

- **CatalogOrderTypes**: A catalog table to store different types of elevator orders.

- **CatalogOrderMovements**: A catalog table to store various movements or directions an elevator can move in (e.g., up, down, rest).

- **CatalogOrderStatus**: A catalog table to store the status of an elevator order.

Each class represents a table in the database. They have been designed using SQLAlchemy's ORM capabilities and include attributes corresponding to columns in the respective tables. Additionally, relationships between different tables are also defined using SQLAlchemy's `relationship` function.

## Significance of Fields for Machine Learning Model

When training a machine learning model to predict the resting floor of an elevator, it's essential to use relevant features that can provide significant predictive power. The fields in the `Elevators`, `ElevatorOrders`, and `ElevatorStatus` tables possess properties that can be invaluable for such a task.

### Elevators

- **elevators_name**: The name or ID of the elevator can provide historical data about the elevator's common stopping or resting floors.

- **elevators_details**: Any specific details about the elevator might indicate certain patterns or behaviors linked with specific floors.

- **elevators_floors**: The total number of floors the elevator serves is crucial. It sets the boundary conditions for our prediction.

- **elevators_rooms**: The number of rooms or offices on each floor can correlate with traffic and subsequently with resting floors, especially during peak hours.

- **elevators_state**: This can give insights into the elevator's current operational state, which can influence its stopping behavior.

- **elevators_created_on & elevators_update_on**: Timestamps can be instrumental in recognizing patterns during specific times of the day, week, or year.

### ElevatorOrders

- **elevator_order_demand_category**: Categories of demand can hint at the type of users or purposes of the elevator trip, influencing the resting floor.

- **elevator_order_demand_type**: Similar to demand category, the type of demand might provide insights into frequent stops.

- **elevator_order_demand_floor & elevator_order_current_floor**: These fields provide a snapshot of where the demands are coming from and where the elevator currently is, which can be used to predict where the elevator might rest next.

- **elevator_order_movement_status & elevator_order_request_status**: The movement and request status can offer insights into the elevator's current operations and the nature of requests it's receiving.

- **elevator_order_created_on & elevator_order_update_on**: Understanding the frequency and timing of orders can help predict busy hours and subsequently potential resting floors.

### ElevatorStatus

- **elevator_status_movement**: Current movement direction can be a strong predictor, especially when combined with order data.

- **elevator_status_current_floor & elevator_status_final_floor**: Knowing the elevator's current and final destination floors is pivotal in predicting its resting floor.

- **elevator_status_created_on**: Timestamps can help identify patterns based on time-based behaviors.

The combination of these features provides a holistic view of the elevator's operations, demands, and behaviors. By training a model on this data, we can potentially predict the elevator's resting floor with higher accuracy, taking into account various influencing factors.
This narrative offers an understanding of how the fields from the mentioned tables can play a pivotal role in predicting the elevator's resting floor.

## Elevator Router

### Router execution

- **elevator_router**: An instance of the FastAPI APIRouter, which will be used to define endpoints related to elevator functions.


### Elevator API Endpoints

#### POST `/elevator/demand`
- Allows a user to place a demand for the elevator.
- **Parameters**:
  - `demand_data`: Contains data such as the elevator ID, current floor, and movement status.
- **Returns**: The current elevator demand after processing the user's request.

#### PUT `/elevator/demand`
- Updates the demand for the elevator.
- **Parameters**:
  - `update_data`: Contains data to update the elevator's demand.
- **Returns**: The updated elevator demand.

#### DELETE `/elevator/demand`
- Deletes a specific demand for the elevator.
- **Parameters**:
  - `delete_data`: Contains data about the elevator demand to delete.
- **Returns**: The current elevator demand after the deletion.

#### POST `/elevator/status`
- Adds a new status entry for the elevator.
- **Parameters**:
  - `demand_data`: Contains data such as the elevator ID and its current status.
- **Note**: This function doesn't return any data but logs the success of the operation.

### Exception Handling
All API endpoints incorporate robust error handling:
- **DatabaseError**: Catches and logs errors related to the database.
- **ServerError**: Catches and logs unexpected errors, providing feedback to the user.



