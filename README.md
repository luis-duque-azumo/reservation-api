# Reservation API

This repository contains a reservation API service that can be run using Docker.

## Getting Started with Docker

### Prerequisites

- Docker installed on your system
- Git to clone this repository

### Building the Docker Image

To build the Docker image, run the following command from the root directory of the project:

```bash
docker build -t reservation-api .
```

### Running the Docker Container

To run the container, use the following command:

```bash
docker run -p 8000:8000 -e API_KEY=mykey reservation-api
```

This will:
- Map port 8000 from the container to port 8000 on your host machine
- Set the API_KEY environment variable to "mykey"
- Start the reservation API service

The API should now be accessible at http://localhost:8000/docs
