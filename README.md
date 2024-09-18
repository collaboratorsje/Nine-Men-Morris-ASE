# Nine-Men-Morris-ASE
Advanced Software Engineering (CS5551) - Project Repository

Team Members: Han Zhou, Seth Emery, Roman Hunter, Sai Vignesh

# Nine Men's Morris Project Setup

This project is divided into two parts:
1. **Backend**: Powered by Flask (Python)
2. **Frontend**: Powered by React (JavaScript)

## Prerequisites
Ensure you have the following installed:
- Python 3.8+ (https://www.python.org/downloads/)
- Node.js (https://nodejs.org/en/download/)

## Setup Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/collaboratorsje/Nine-Men-Morris-ASE.git
   cd Nine-Men-Morris-ASE

2. Run the bash script (follow the steps for windows or mac)
# Windows
Run a shell script that installs dependencies and creates virtual environment.
That script on windows is setup.bat

    setup.bat

To start the backend only:

    cd backend
    flask run

To start the backend and frontend concurrently (recommended):

    cd client
    npm start

Open in a browser at http://127.0.0.1:5000 or http://localhost:5000

# Mac
Note: The Mac setup is similar to the Windows setup, but with slight command differences.

Run a shell script that installs dependencies and creates virtual environment.
That script on mac is setup.sh

    chmod +x setup.sh
    ./setup.sh

To start the backend only:

    cd backend
    flask run

To start the backend and frontend concurrently (recommended):

    cd client
    npm start

Open in a browser at http://127.0.0.1:5000 or http://localhost:5000

### **How This Works**

- **For the Backend:**
  - The script will create and activate a Python virtual environment in the `backend` directory.
  - It will install the backend dependencies from the `requirements.txt` file.

- **For the Frontend:**
  - The script will navigate to the `client` folder and run `npm install` to install the frontend dependencies.
