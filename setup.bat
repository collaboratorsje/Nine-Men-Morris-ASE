@echo off
echo Setting up the project...

:: Backend setup
cd backend
echo Creating virtual environment for backend...
python -m venv venv
call venv\Scripts\activate
echo Installing backend dependencies...
pip install -r ../requirements.txt
cd ..

:: Frontend setup
cd client
echo Setting up frontend...
npm install
cd ..

echo Setup complete!
echo To start the backend, navigate to backend and run "flask run".
echo To start the frontend and backend concurrently, navigate to client and run "npm start".
