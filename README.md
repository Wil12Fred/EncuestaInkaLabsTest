## A Django Rest Framework: authentication example + 'encuesta' management

### Functionality:

* [x] Login
* [x] Registration
* [x] Password Change
* [x] Encuesta management: Alternativa, Pregunta, Encuesta

### How to use:

- Clone the repo

#### Backend
1. cd backend & pipenv shell & pipenv install
2. python3 manage.py makemigrations custom_user
3. python3 manage.py makemigrations encuesta
4. python3 manage.py migrate
5. python3 manage.py createsuperuser
6. python3 manage.py runserver

### Based on

* https://github.com/opmftw/react-django-login-example
