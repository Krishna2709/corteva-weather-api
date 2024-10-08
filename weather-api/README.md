# Project Directory Overview

The project contains multiple files and directories, each serving a specific purpose in developing, testing, and running the weather API. Below is a description of each file and directory and their roles.

## Project Structure

```
weather-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── crud.py
│   ├── schemas.py
│   ├── deps.py
│   ├── database.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── weather.py
│   │   │   ├── weather_stats.py
├── tests/
│   ├── __init__.py
│   ├── test_weather_api.py
├── scripts/
│   ├── data_ingestion.py
│   ├── analyze_data.py
├── .github/
│   └── workflows/
│       └── ci.yml  # Continuous Integration workflow
├── Dockerfile
├── requirements.txt
├── README.md
└── .flake8  # Linter configuration file
```

---

## Description of Each File and Directory

### `app/`
This folder contains the main application logic, including the FastAPI routes, models, database setup, and CRUD operations.

- **`__init__.py`**: Initializes the `app` package. This file allows the folder to be treated as a Python package.
  
- **`main.py`**: The entry point of the FastAPI application. It defines the app object, includes the API routes, and ensures that database tables are created when the app starts.

- **`models.py`**: Contains the SQLAlchemy models, which define the structure of the database tables, such as `WeatherData` and `WeatherStation`.

- **`crud.py`**: Contains functions that interact with the database to perform Create, Read, Update, Delete (CRUD) operations. These functions handle data fetching and modifications.

- **`schemas.py`**: Contains Pydantic models, which define the structure of the data that the API sends or receives. They validate the incoming requests and format the outgoing responses.

- **`deps.py`**: Contains reusable dependencies that can be injected into the routes. For example, it contains a function to get the database session.

- **`database.py`**: Manages the database connection using SQLAlchemy. It includes logic for setting up the connection to the database and handling sessions.

#### `app/api/`
This folder defines the API endpoints for the project.

- **`__init__.py`**: Initializes the `api` package.

- **`v1/`**: This folder contains the version 1 (`v1`) of the API routes.
  
  - **`weather.py`**: Defines the `/weather` endpoint, which returns weather data, optionally filtered by station ID and date.
  
  - **`weather_stats.py`**: Defines the `/weather/stats` endpoint, which returns calculated weather statistics like average temperatures and total precipitation.

### `tests/`
This folder contains test files for the project, ensuring the API works as expected.

- **`__init__.py`**: Initializes the `tests` package.
  
- **`test_weather_api.py`**: Contains unit tests for the weather and weather statistics API endpoints. These tests verify that the API responds with the correct data and status codes.

### `scripts/`
This folder contains utility scripts used for data processing.

- **`data_ingestion.py`**: This script reads weather data files, processes them, and ingests them into the database. It avoids inserting duplicate records and logs the ingestion process.

- **`analyze_data.py`**: This script calculates yearly weather statistics (such as average maximum temperature and total precipitation) for each weather station and stores them in the database.

### `.github/`
This folder contains configuration files for GitHub Actions, which are used for Continuous Integration (CI) and Continuous Deployment (CD) pipelines.

- **`workflows/ci.yml`**: This defines a GitHub Actions workflow for running tests, linting code, and checking the project's format whenever code is pushed to GitHub.

### `Dockerfile`
This file contains the instructions on how to build a Docker image for the project. Docker allows the application to run in a consistent environment across different machines. This file describes setting up the environment, installing dependencies, and starting the FastAPI server inside a Docker container.

### `requirements.txt`
A list of Python dependencies that are required for the project. It includes libraries like FastAPI, SQLAlchemy, and Pydantic. When setting up the project, you can install these dependencies using `pip install -r requirements.txt`.

### `README.md`
This file contains an overview of the project, instructions for installing and running it, and any other important information needed by developers or users to understand and use the project.

### `.flake8`
This is the configuration file for `flake8`, a code linting tool. It defines the rules and settings for linting the Python code in the project, such as the maximum line length and which files or directories to ignore.

---

## Summary

- **`app/`**: Main application code, including the FastAPI setup, models, and routes.
- **`tests/`**: Unit tests to validate the API's functionality.
- **`scripts/`**: Scripts for ingesting and analyzing weather data.
- **`.github/`**: CI/CD pipeline configuration using GitHub Actions.
- **`Dockerfile`**: Defines how to build a Docker image for the project.
- **`requirements.txt`**: List of Python dependencies.
- **`README.md`**: Overview and instructions for the project.
- **`.flake8`**: Linting configuration for maintaining code quality.

This structure ensures the project is well-organized, easy to maintain, and scalable. Each file has a clear role in developing, testing, deploying, and supporting the weather data API.

## Endpoints Testing

FastAPI's built-in Swagger UI
- run `uvicorn app.main:app --reload`
- Access Swagger UI: `http://127.0.0.1:8000/docs`
- Test the **/api/v1/weather** endpoint with these params:
```
station_id: Filter by station ID (e.g., USC00110072)
date: Filter by date (e.g., 1985-01-19)
skip: Number of records to skip for pagination.
limit: Number of records to return.
```
- Test the **/api/v1/weather/stats** endpoint with these params:
```
station_id: Filter by station ID (e.g., USC00110072)
year: Filter by year (e.g., 1985)
skip: Number of records to skip for pagination.
limit: Number of records to return.
```

## Deployment on AWS

I will be using the following AWS services to host this app - 

- RDS (PostgreSQL): Managed database service for weather data hosting.
- API Gateway: Provide a scalable, managed REST API endpoint.
- EC2 or AWS Lambda: This hosts the ingestion and API code.
- ALB: For load balancing.
- S3: Store raw weather data files for long-term storage and ingestion automation.
- CloudWatch: Monitor logs and schedule ingestion tasks with CloudWatch Events or Lambda scheduled functions.
