#!/bin/bash

echo "Setting up the project..."

# Backend setup
echo "Creating virtual environment for backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
echo "Installing backend dependencies..."
pip install -r ../requirements.txt

# Frontend setup
echo "Setting up frontend..."
cd ../client
npm install

echo "Setup complete!"
echo "To start the backend, navigate to backend and run 'flask run'."
echo "To start the frontend and backend concurrently, navigate to client and run 'npm start'."
