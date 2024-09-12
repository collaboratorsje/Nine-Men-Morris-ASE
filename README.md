# Nine-Men-Morris-ASE
Advanced Software Engineering (CS5551) - Project Repository

Team Members: Han Zhou, Seth Emery, Roman Hunter, Sai Vignesh

# Requirements
Python 3.x

# Windows
Pull Repository

git clone https://github.com/collaboratorsje/swe-capstone.git
Virtual Environment Setup

cd Nine-Men-Morris-ASE
    python -m venv venv 
Activate Virtual Environment (Must do every time you launch, you'll see (venv) in your terminal)

    .\venv\Scripts\Activate.ps1 # If using Powershell
or

    .\venv\Scripts\activate.bat # If using Command Prompt

Install Requirements

    python -m pip install -r .\requirements.txt

Launch with

    flask run

Open in browser at http://127.0.0.1:5000 or http://localhost:5000

# Mac
Note: The Mac setup is similar to the Windows setup, but with slight command differences.

Virtual Environment Setup

    python3 -m virtualenv venv

Activate Virtual Environment (Must do every time you launch, you'll see (venv) in your terminal)

    source ./venv/bin/activate

Install Requirements

    python3 -m pip install -r ./requirements.txt

Launch with

    flask run
    
Open in browser at http://127.0.0.1:5000 or http://localhost:5000
