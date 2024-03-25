# RoomPriceGenie Test Task

## Description

This project is a test task for RoomPriceGenie. It implements an API for managing hotel room booking data, including adding and retrieving booking events, and provides a dashboard with aggregated information on bookings.

## Technologies

The project uses the following technologies and tools:

- Django and Django REST Framework for web application and API creation.
- Celery for asynchronous task processing.
- Redis as a message broker for Celery.
- Docker and Docker Compose for containerization and local deployment.
- PostgreSQL as the primary database.

## Installation and Launch

Docker and Docker Compose are required to run the project.

### Project Launch

1. Clone the repository:
   ```bash
   git clone https://github.com/Rasulid/RoomPriceGenie_test_task.git
   cd RoomPriceGenie_test_task
   
2. Create .env configuration file:
   create a file based on .env.example
    ```bash
   cp .env.example .env

3. Build and up docker container:
   ```bash
   docker-compose up --build
   ```
   or 
   ```bash
   docker-compose build
   dcoker-compose up -d
   ```
   flag -d it means docker up in background 

API documentation is available at http://localhost:8000/swagger/ after launching the project, 
where you can test different endpoints.

### Testing
Run the tests by executing the following command inside the web container:

```bash
   docker-compose exec web python manage.py test