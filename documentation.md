# Documentation for the Citric Sheep Application

## Table of Contents

1. [Libraries](#libraries)
2. [Logger Configuration](#logger-configuration)
3. [APP Configuration](#app-configuration)
4. [APP Main Routers](#app-main-routers)

---

## Libraries

- **logging**: The built-in Python library used for logging application events.
- **FastAPI**: A modern, fast web framework for building APIs with Python 3.7+. 
- **configure_project_attributes**: This module from our configuration folder contains details related to the project's attributes.
- **elevator_router**: From the `apps.elevator` package, this module is responsible for routes related to the elevator functionality of the application.
- **os**: Interact with the operating system. Used for getting paths, environment variables, etc.
- **dotenv**: A library to load environment variables from a `.env` file.

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