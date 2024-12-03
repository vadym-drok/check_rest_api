# FastAPI Receipts Service

This project is a REST API service implemented using [FastAPI](https://fastapi.tiangolo.com/). It includes functionality for managing users and receipts using a PostgreSQL database.  
The service allows users to register, authenticate, create, and view receipts.

## Requirements for Launch

1. Docker and Docker Compose (for containerization).
2. Python 3.9 (if you want to run the project locally).
3. Configuration file `.env` containing environment variables (use `.env_example` as example)

## Launch Instructions

1. **Clone the repository**:

2. **Start Docker containers**:
   Make sure you have Docker and Docker Compose installed.
   
   Run the command:
   ```bash
   make install
   ```
   This command will start PostgreSQL, PgAdmin, and the FastAPI service.

3. **Access the service**:
   
   After starting, the service will be available at: [http://localhost:8003/](http://localhost:8003/). Here, you will find the API documentation (Swagger).  
   Also, you can view DB with [pgAdmin](http://127.0.0.1:5050/).

4. **Testing**:
   
   You can run tests using the command:
   ```bash
   make run-tests
   ```
 
## Using the API

- **User Registration**:
  `POST /users`
- **User Authentication**:
  `POST /login`
- **Create Receipt**:
  `POST /receipts`
- **Get List of Receipts**:
  `GET /receipts`

Detailed description of all available routes can be found in the Swagger documentation at [http://localhost:8003/](http://localhost:8003/).

## Important Notes

- **Configuration**: The `.env` configuration file must be set up before running the service. Make sure to correctly specify all necessary environment variables.
- **Test Database**: Separate databases are used for running tests, which are automatically created and dropped using pytest fixtures.

## Dependencies

The project uses the following libraries and frameworks:

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PyJWT](https://pyjwt.readthedocs.io/)
- [Docker](https://www.docker.com/)

To install all dependencies locally, use:
```bash
pip install -r requirements.txt
```

## Development

To run the server locally for development:

1. Install all dependencies.
2. Start the server using [uvicorn](https://www.uvicorn.org/):

    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
    ```

