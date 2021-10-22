# StudentSublease Backend
This is the backend for Team Coder's mobile apps and services project.

## Installation

### Requirements
- Python 3.8 with pip and virtualenv

### Setup
1. Clone the git repo ```git clone https://github.com/ryantobin77/StudentSublease_Backend.git```
2. Navigate into the root directory ```cd path/StudentSublease_Backend/StudentSublease_Backend```
3. Initialize the virtualenv with ```virtualenv venv```
4. Activate the virualenv with ```source venv/bin/activate```
5. Install all requirements ```pip install -r requirements.txt```
6. **Only do this once**. Setup the database by running ```python manage.py setup_db```

### Running the backend
Anytime you run the mobile app, the backend must also be running. From the root directory, with virtualenv activated, run:
```bash
python manage.py runserver
```
You should be all setup!

### APIs Available
