# Data Processor App

Welcome to Vincent's data_processor_app repository! This README will guide you through the steps required to clone the repository, set up the environment, and run both the React frontend and the Django backend locally to test out the app.

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
git clone https://github.com/vincentarsontaneli/data-processor-app.git
cd data-processor-app
```


### FRONTEND
Navigate to the frontend directory and install the npm dependencies:
```
cd data_processor_app_frontend
npm install
npm start
```
The React app should now be running, typically accessible at http://localhost:3000.



### BACKEND
cd ../data_processor_app_backend
python -m venv env

.\env\Scripts\activate
source env/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

The Django server should now be running on http://127.0.0.1:8000/.


### Final Checks
Ensure that the `apiURL` var in the `FileUploadCard` component is set to the same link to your live local Django server.
Ensure that the `CORS_ALLOWED_ORIGINS` list contains your live react app link in `data_processor_app_backend/data_processor_app_backend/settings.py`.

## Comments

This project has presented diverse challenges, from developing a full-stack application from the ground up within a tight timeframe to evaluating optimal data inference logic for handling various datasets, each with unique characteristics.

It is recommended to feed the app with a dataset with at least 50 rows so that there's enough information for the app to accurately infer the types.

There are certainly room for improvement in the backend logic to infer the data types more accurately. I also havent test it for extremely large datasets with millions of rows, or explored more granular data types.