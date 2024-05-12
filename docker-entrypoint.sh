#!bin/bash

echo "Starting authentication service"

uvicorn main:app --host 0.0.0.0 --port 81