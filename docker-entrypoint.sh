#!/bin/bash

echo "Starting authentication service"

# Run Alembic migrations
alembic upgrade head

# Start the application with the appropriate port
uvicorn main:app --host 0.0.0.0 --port 5000
