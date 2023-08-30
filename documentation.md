# Documentation for the Citric Sheep Application

---

## Libraries

- **logging**: The built-in Python library used for logging application events.
- **FastAPI**: A modern, fast web framework for building APIs with Python 3.7+. 
- **os**: Interact with the operating system. Used for getting paths, environment variables, etc.
- **dotenv**: A library to load environment variables from a `.env` file.
- **sqlalchemy**: The SQL Toolkit and Object-Relational Mapping (ORM) library for Python. We are importing functionalities to create an engine and manage sessions.
- **uvicorn**: A lightning-fast ASGI server implementation, using uvloop and httptools.
- **psycopg2**: A PostgreSQL database adapter for Python.
- **pydantic**: Data validation and settings management using Python type hinting.
- **pathlib**: A library for representing the file system path semantics of different operating systems.
- **typing**: Support for type hints.
- **enum**: Support for enumerations.
- **alembic**: A database migration tool for SQLAlchemy.
- **pytest**: A framework that makes it easy to write small tests, yet scales to support complex functional testing for applications and libraries.

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

## Elevator Logic

### Direction Enumeration
Defines the possible directions an elevator can move in.
- **STATIONARY**: Elevator is not moving.
- **DOWN**: Elevator is moving downwards.
- **UP**: Elevator is moving upwards.

### Elevator Class
This class represents the elevator, with attributes for its current floor, direction of movement, and request queue.

#### Methods:
- **__init__**: Initializes an elevator instance with a given request queue, direction, and current floor.
- **target_floor**: Determines the target floor for the elevator based on current direction and request queue. This method handles various scenarios like if the elevator is moving upwards and there's a request above its current floor or if it's moving downwards and there's a request below.

## Alembic Configuration and Migrations Script

### Configuration

The script starts by obtaining configurations from Alembic's Config object which provides access to the values within the `.ini` file being used. The SQL Alchemy URL for the database is also set from `db_sqlalchemy_url`.

If a `config_file_name` is set, it sets up loggers for the application. The target metadata for our migrations is taken from `BaseModel.metadata`.

### Running Migrations

#### Offline Mode
In the 'offline' mode, migrations run without the need for an Engine or even a DBAPI. The context gets configured using only a URL. It will emit the generated SQL to the script output.

#### Online Mode
For the 'online' mode, an Engine is required, and a connection is associated with the context. It establishes a connection and then starts the migration process.

### Execution

The script checks if the context is in `offline` mode. If true, it calls the `run_migrations_offline()` function, otherwise, it calls `run_migrations_online()`.

## Test Configuration and Setup

### Configuration 

The database configurations are fetched using the `configuration.configure_bd_test_credentials.DB_URL`. An engine is then created using SQLAlchemy's `create_engine` method. A session for database operations is created using the `sessionmaker` method from SQLAlchemy.

`start_application` function initializes a new FastAPI application and includes the elevator router in it.

### Database Test Functions

1. **app**: This pytest fixture is of module scope. It does the following:
   - Initializes the database with all the tables and relationships defined in `BaseModel`.
   - Starts the database session.
   - Applies all migrations from Alembic.
   - Fills the database with test data from `catalogs_data.catalog_data`.
   - Yields the FastAPI application for testing.
   - Drops all tables after the tests are complete.

2. **db_session**: A function-scoped pytest fixture. This creates a new database session for each test. After the test, the session is closed, and the transaction is rolled back, ensuring a clean state for the next test.

3. **client**: Another function-scoped pytest fixture. This fixture:
   - Overrides the database connection dependency in the FastAPI application to use the test session.
   - Yields a test client for the application. This client can be used in tests to make requests to the application.

These fixtures ensure a clean and isolated environment for each test, making sure tests do not interfere with each other.

## General Considerations for a Machine Learning Model for Resting floor Prediction

The current architecture and data collection setup have several distinct advantages that make it highly suitable for training a machine learning model geared towards predicting the resting floor of an elevator. Here's why:

## 1. Detailed Data Collection:
- The database models are intricate and capture every facet of the elevator's operations. This high granularity ensures the model gets a holistic view, vital for discerning intricate patterns.

## 2. Time-Stamped Data: 
- Timestamps (`elevator_order_created_on`, `elevator_order_update_on`, etc.) allow the model to discern temporal patterns, such as predicting resting floors during off-peak hours.

## 3. Relational Data Insights: 
- The use of foreign keys and relationships means the model can understand the interactions between different entities (like elevators and their orders), allowing for richer behavioral pattern recognition.

## 4. Categorization and States:
- Categorized data from tables like `catalog_elevator_states` and `catalog_order_movements` provide vital context. These categories can significantly influence predictive accuracy when used as features.

## 5. Elevator Logic Implementation:
- The existing `Elevator` class logic ensures the model builds on foundational rules, enhancing the learning process's efficiency and accuracy.

## 6. Versatility:
- The system's focus on both current elevator states and their dynamic orders ensures a model trained here understands both static and dynamic patterns, enriching its predictive prowess.

## 7. Real-world Scenario Handling:
- With logic that accounts for direction (`STATIONARY`, `DOWN`, `UP`), the model will be adept at making predictions grounded in real-world scenarios.

## 8. Feedback Loop Potential: 
- The architecture allows for a feedback loop, enabling continuous model optimization by comparing the model's predictions against actual outcomes.

## 9. Data Ingestion for ML:
- Given the structured nature of the database models and the relationships between them, it makes data ingestion for machine learning seamless. Machine learning models require clean, structured data, and the current setup ensures that data fed into the model is consistent, reducing the need for extensive preprocessing. This not only speeds up the training process but also enhances model accuracy.

Also while it's early to comment which model would be better for this use case, It could be recommended two options given the nature of the problem, a supervised model or a time series forecasting model. The supervised model would be trained on the historical data to predict the resting floor of an elevator. The time series forecasting model would be trained on the historical data to predict the resting floor of an elevator at a specific time in the future. Both models would be trained on the same data and evaluated on the same metrics to determine which one is better suited for the use case.

The way this data is stored makes this app viable to even implement the ML model because it can be done by adding endpoints throught other routers from the same base, via a clean table that has been preprocessed to be used by the ML model. taking advantage of the database connection via dependency injections like it has been already used in the current endpoints.

Getting into more technical details, one first has to investigate how the data behaves before choosing a model, for example if we go by a supervised model, we have to see the frequency of the predictions in pair with the complexity, this will be closely associated with the complexity of the elevator use, for example it's not the same having to predict a resting floor for a building that has a low demand (and this implies less data to train) that a high concurrence building, where the data is more complex and the predictions are more recurrent.

For a Time Series Forecasting model is the same, the complexity of the data will determine the complexity of the model, and the complexity of the model will determine the complexity of the data, so it's a matter of finding the right balance between the two. it's not the same to use for example an ARIMA model for a building with low demand than a Prophet model or even a Neural Network (RNN, LSTM, GRU) for a building with high demand.

With this in mind, collecting all the posible data that a normal elevator could provide in an structure way with some external data and fields where more data could be store in the future make this a good approach for the problem.