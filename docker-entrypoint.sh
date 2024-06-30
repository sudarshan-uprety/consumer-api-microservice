#!/bin/bash

echo "Starting authentication service"

# Set the port based on the environment
case "$ENV" in
  "prod")
    PORT=9002
    ;;
  "uat")
    PORT=9001
    ;;
  "dev")
    PORT=9000
    ;;
  *)
    echo "Unknown environment: $ENV"
    exit 1
    ;;
esac

# Run Alembic migrations
alembic upgrade head

# Start the application with the appropriate port
uvicorn main:app --host 0.0.0.0 --port $PORT
