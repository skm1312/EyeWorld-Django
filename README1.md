## EyeWorld-Django

**E-commerce Web Application with Facial Shape Recognition with no payment page**

This Web App was built as a final project for the CS 876 Software Engineering Class, University of Regina, Canada.

## Live Demo

**Follow this link to view deployed version of the web app https://eyeworld.herokuapp.com/**


## Deployment / Hosting

This Project was deployed and is hosted on Heroku from GitHub

## Databases / Static Files

When running locally, SQLite database was used & static and media files were stored locally. 
When deploying, Heroku Postgres was used as the server database, Gunicorn and Whitenoise was set 
up to host all the static files.

## Installation

Follow the below instructions to clone this project

1. Go to folder you want to put the cloned project in your terminal & type:
    `git clone https://github.com/skm1312/EyeWorld-Django`
2. Create & Activate a new Virtual Environment in terminal:
    Create: `virtualenv venv .`
    Activate: `./Scripts/activate/`
3. Install the project dependancies:
    `pip install -r requirements.txt`
4. In the terminal:
    `python manage.py migrate` - this will apply migrations to your local sqlite database
    `python manage.py createsuperuser` - this will create admin support
    `python manage.py runserver` - this will start a local server
5. Go to your browser & type '127.0.0.1:8000' in the address bar
6. Log in to the admin panel by going to '127.0.0.1:8000/admin' & log in using the credentials you created for the superuser
7. You can add products, product categories and uers from here

## Note

** The requirements.txt file has been elimated of all sensitive information, the steps to update it for your cloned project will be added shortly **
