# Project Name

Welcome to the Project Name repository! This README will guide you through the steps required to clone the repository, set up the environment, and run both the React frontend and the Django backend locally.

## Prerequisites

Make sure you have the following installed on your machine:

- [Git](https://git-scm.com/)
- [Node.js](https://nodejs.org/) (which includes npm)
- [Python](https://www.python.org/) (Ensure Python 3.6+ is installed)
- [pip](https://pip.pypa.io/en/stable/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/)

## Clone the Repository

First, clone the repository to your local machine using Git:

```
git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
```


FRONTEND
Navigate to the frontend directory and install the npm dependencies:
cd frontend
npm install
npm start

BACKEND
cd ../backend
python -m venv env

.\env\Scripts\activate
source env/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

The Django server should now be running on http://localhost:8000/.

