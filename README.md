## A Django Rest Framework: authentication example + 'encuesta' management

### Functionality:

* [x] Login
* [x] Registration
* [x] Password Change
* [x] Encuesta management: Alternativa, Pregunta, Encuesta

### How to use:

- Clone the repo

[requires]
python_version = "3.7"
pipenv, version 2018.11.26 (pip install pipenv)

#### Backend
1. cd backend & pipenv shell & pipenv install
2. python3 manage.py makemigrations custom_user
3. python3 manage.py makemigrations encuesta
4. python3 manage.py migrate
5. python3 manage.py createsuperuser
6. python3 manage.py runserver

### Based on

* https://github.com/opmftw/react-django-login-example
