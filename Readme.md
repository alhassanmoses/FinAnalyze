

# FinAnalyze(Financial Analytics) API Documentation

## Introduction

This documentation outlines the design, development, and deployment of the FinAnalyze(Financial Analytics) API, a RESTful API built using FastAPI. The API focuses on managing user financial records, transaction analytics, and asynchronous processing. The following sections provide details on setting up and running the API, architectural decisions, testing, containerization, and potential scaling strategies.

## Table of Contents

- [FinAnalyze(Financial Analytics) API Documentation](#finanalyzefinancial-analytics-api-documentation)
  - [Introduction](#introduction)
  - [Table of Contents](#table-of-contents)
  - [1. Setup and Run Instructions](#1-setup-and-run-instructions)
    - [Prerequisites](#prerequisites)
    - [Installation and Usage](#installation-and-usage)
    - [Manual Setup](#manual-setup)
    - [Using Docker](#using-docker)
  - [2. Design and Architectural Decisions](#2-design-and-architectural-decisions)
    - [API Endpoints](#api-endpoints)
    - [Transaction Analytics](#transaction-analytics)
    - [Asynchronous Processing](#asynchronous-processing)
  - [3. Testing with Pytest](#3-testing-with-pytest)
  - [4. Containerization with Docker](#4-containerization-with-docker)
  - [5. Scaling Strategies](#5-scaling-strategies)
  - [6. Data Security and Privacy](#6-data-security-and-privacy)
  - [7. Monitoring and Logging](#7-monitoring-and-logging)
  - [8. Continuous Integration and Deployment (CI/CD)](#8-continuous-integration-and-deployment-cicd)
  - [9. Conclusion](#9-conclusion)

## 1. Setup and Run Instructions

### Prerequisites

Before running the FinAnalyze API, ensure you have the following prerequisites installed:

- Python 3.x
- Docker (for containerization)
- [FastAPI](https://fastapi.tiangolo.com/)
- [pytest](https://docs.pytest.org/en/latest/)

### Installation and Usage

To set up and run the API:

___Kindly create a `.env` file in the `backend` directory and copy-paste all the contents of `.env.example` into it to avaoid any issues due to missing environment variables___.

1. Clone this repository to your local machine.

2. Navigate to the project directory.


### Manual Setup
1. Move into the backend directory: ```cd backend```
   
2. Install the required dependencies:
```pip3 install pipenv```
or ```pip install pipenv``` (___whichever works___)

3. Activate your virtual environment:```pipenv shell```
   
4. Run the FastAPI application:
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

5. Access the API documentation at `http://localhost:8000/api/v1/docs` or the OpenAPI JSON at `http://localhost:8000/openapi.json` in your web browser or API client. You can also try a less cluttered documentation view here ```http://localhost:8000/external-api/v1/docs```

### Using Docker

1. Move into the backend directory: ```cd backend```

2. Make sure all the scripts are executable on your local machine, you can use the following command to make all the scripts in the _scripts_ directory executable:
   ```chmod +x scripts/*.sh``` 

3. To start the application simply run this command to execute the start script: ```./scripts/start.sh```

4. To SSH into the API container instance, use the comman: ```./scripts/bash.sh``` 

5. To run test use the command ```./scripts/bash.sh``` then ```pytest tests/test_*.py``` when you're within the docker instance.

6. There is another script to directly run all test but it tends to be slow rightnow, _my bash scripting skills are not very solid yet_ : ```./scripts/run_tests.sh```

7. Press `Ctrl + C` to ___gracefuly___ terminate the running application along with the active container instance.

## 2. Design and Architectural Decisions

### API Endpoints

The API offers the following endpoints for managing financial records:

- `POST /api/v1/transaction/create`: Create a new transaction record.
- `GET /api/v1/transaction/{transaction_id}`: Read a transaction record.
- `GET /api/v1/transaction/all`: Retrieve all records of the requesting user's transactions(___transaction history___).
- `PUT /api/v1/transaction/update/{transaction_id}`: Update a transaction record.
- `DELETE /api/v1/transaction/delete/{transaction_id}`: Delete a transaction record.
- `GET /api/v1/transaction/analytics/{user_id}`: Delete a transaction record.

Each record includes `user_id`, `full_name`, `transaction_date`, `transaction_amount`, and `transaction_type` (credit/debit).

Auth Endpoints

- `POST /api/v1/user/sign_up`: Create a user account.
- `POST /api/v1/user/login`: Generates a JWT token.

### Transaction Analytics

This API provides the `GET /api/v1/transaction/analytics/{user_id}` endpoint, which retrieves a user's average transaction value and the day with the highest number of transactions.

### Asynchronous Processing

Asynchronous processing is implemented throughout the application especially when db persist calls are made, it feels a bit dangerous with the way FastAPI handles threads db threads but most edge cases have been accounted for. Strategies for enhancing system responsiveness and efficiency have been considered in my current design and implementation.

## 3. Testing with Pytest

Unit tests using Pytest have been included to ensure the correctness and reliability of the APIs. These tests cover primary use cases and edge cases, helping maintain the API's stability over time.

To run the tests, execute the following command:
pytest
## 4. Containerization with Docker

A Dockerfile is provided to containerize the FastAPI application. The Docker container runs the application smoothly and can be easily integrated with databases and external systems.

To build and run the Docker container(___Refer to the Using Docker section above for a simpler process___):

1. Build the Docker image:
docker build -t FinAnalyze-api .
2. Run the Docker container:
docker run -p 8000:8000 FinAnalyze-api
## 5. Scaling Strategies

This API has been designed with scalability in mind. Potential strategies for scaling the solution for a substantial user base include:

- Load balancing using a reverse proxy.
- Implementing a database sharding or clustering strategy.
- Caching frequently accessed data.
- Adopting microservices architecture for better resource management.

Considerations and trade-offs for each strategy have been outlined for future reference.

## 6. Data Security and Privacy

Data security and privacy are paramount. The API should be configured with proper authentication and authorization mechanisms to protect sensitive user financial data. Ensure that sensitive data is encrypted and stored securely, and that access controls are in place.

## 7. Monitoring and Logging

For effective maintenance and troubleshooting, a comprehensive logging system has been implemented to record relevant events and errors, facilitating debugging and auditing. Other monitoring and logging solutions were considered but they're honestly not needed rightnow hence they have've not been integrated. In the future, I do think it would be fun to include some of those integration to Monitor API performance, resource utilization, and error rates ___for the fun of it___.

## 8. Continuous Integration and Deployment (CI/CD)

To maintain code quality and streamline deployments, setting up a CI/CD pipeline was considered, but seeing as this project may not be deployed anytime soon, that has been brushed off. Automations for the testing and deployment processes, to ensure that new features and updates are released reliably, may be added in the future if I decide to revisit this.

## 9. Conclusion

The FinAnalyze API is a robust solution for managing financial transactions and user interactions. Its design decisions, scalability strategies, and testing ensure its reliability and performance in production environments. Continuous improvement, monitoring, and adherence to best practices are key to maintaining a successful financial services API.

For any further inquiries or support, please contact me [alhassanmoses.amw@gmail.com](mailto:alhassanmoses.amw@gmail.com).

Thank you for your attention, and I look forward to positive feedback!