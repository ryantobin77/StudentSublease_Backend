# StudentSublease Backend
This is the backend for Team Coder's mobile apps and services project.

## Installation

### Requirements
- Python 3.8 with pip and virtualenv
- Install Redis (See Configure Messaging below)

### Setup
1. Clone the git repo ```git clone https://github.com/ryantobin77/StudentSublease_Backend.git```
2. Navigate into the root directory ```cd path/StudentSublease_Backend/StudentSublease_Backend```
3. Initialize the virtualenv with ```virtualenv venv```
4. Activate the virualenv with ```source venv/bin/activate```
5. Install all requirements ```pip install -r requirements.txt```
6. Make any migrations ```python manage.py makemigrations```
7. Run any migrations ```python manage.py migrate```
8. **Only do this once**. Setup the database by running ```python manage.py setup_db```

## Configure Messaging
Messaging uses websockets to allow for real time communication between users. This real time communication uses
Redis as a backing store. Install redis for messaging:

```
brew install redis
```

Before running the python server, in a separate terminal window, run:

```
redis-server
```

### Running the backend
Anytime you run the mobile app, the backend must also be running. From the root directory, with virtualenv activated, run:
```bash
python manage.py runserver
```
You should be all setup!

### APIs Available
