# Dep-Map-App

The term base used for Sqlite3 Db is been extracted and developed at the repository mentioned below:
Refer : https://github.com/Smita1102/Atlas-of-Learning-Project

refer requirements.txt file. 

python 3.7.3 or higher with pip

Whatever you prefer to manage your python dependencies VirtualEnv, Pipenv, Conda or anything that alllows you to use pip install
We are using SQLite3
This is  to be run on Anaconda Promt
preinstallation required-

pip install django
python -m pip install --upgrade pip setuptools wheel

Latest version of pip, pillow , crispy-forms before running the project 
pip install pillow
pip install django-crispy-forms



Setup

Create your virtual enviroment for this I will use Conda 
conda create --name surveyenv pip python=3.7


Activate your virtual environment

activate surveyenv
With your virtual environment active navigate to the root of the project where the manage.py and requirements.txt files are located and execute:

For sqllite3
pip install -r requirements.txt

Add local configuration
Note: You must run the following commands from the root of your project




Running the project
Note: For the following commands you must have already configured your database settings and make sure you have your virtual environment activated. You must also be located on the root of the project

Run migrations

python manage.py migrate

Create super user

python manage.py createsuperuser

Run the server

python manage.py runserver
You should now be able to navigate to http://127.0.0.1:8000/ and start answering some questions as the migrations contains initial data or go to http://127.0.0.1:8000/admin and enter your superuser data to check the answers or add more questions




Have fun 🎉
