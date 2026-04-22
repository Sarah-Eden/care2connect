# Care2Connect

A full-stack web application that aims to improve compliance with recommended health care standards for foster children by providing caseworkers and foster parents with a secure, centralized platform for managing case information and autmatically generating reminders for well child care, immunizations, and routine dental care.

**Security Note** This application does not have HIPAA compliant security measures and should not be used to store any sensitive information or PHI. All data in the screenshots below are mock data created by the developer for testing purposes.

## What It Does

- Stores child demographic, health, and foster placement information and foster family data including maximum capacity.
- Generates recommended well child checkups and immunization records based on the child's age, the American Academy of Pediatrics' Bright Futures guidelines and the CDC's recommended immunization schedule for children under the age of 18.
- Sends email reminders to schedule the appointment to the child's foster parent(s) and caseworker at set intervals prior to the due date. Also displays reminders on the appropriate user's dashboard starting 30 days before it is due.

## Screenshots

| Caseworker View                                                                        |
| -------------------------------------------------------------------------------------- |
| <img src="docs/images/CaseworkerDashboard.jpg" alt="Caseworker Dashboard" width="600"> |

| Foster Parent View |
| ------------------ |

| <img src="docs/images/FosterParentDashboard.jpg" alt="Foster Parent Dashboard" width="600"> |

### Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL
- Git

### Tech Stack

**Frontend**

- React & React Hook Form
- Material-UI components
- Axios for API calls

**Backend**

- Django 5.2 + Django REST Framework
- PostgreSQL database - configured to use local install
- Django-Q for automated tasks

### Initial Setup

1. Clone the repository.
2. Setup the backend and install requirements.txt:

```
cd backend
cp .env.example .env
python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt
```

3. Setup the database:

```
createdb care2connect
python manage.py migrate
python manage.py setup_groups
python manage.py setup_schedules
python manage.py createsuperuser
```

4. In a new terminal, set up the front end and install required packages:

```
cd ../frontend
cp .env.example .env
npm install
```

### Running the App

1. In the backend terminal, start the backend:

```
python manage.py runserver
```

2. In the frontend terminal, start the frontend:

```
npm start
```

3. Open: http://localhost:3000/login

### Additional Information

Django Administration has been configured for this project. To access the database go to http://localhost:8000/admin/ and enter the superuser credentials you created in the setup.

### Running Tests

Backend tests covber model validation, permissions, and health service visit creation logic.

```
cd backend

# Run specific test modules
python manage.py test c2c.tests.auth_tests
python manage.py test c2c.tests.epsdt_tests
python manage.py test c2c.tests.tasks_tests
```
