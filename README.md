# Django Blog

A blog made using django 3, markdown and postgresql. 

Install dependencies :
```
$ pip install -r requirements.txt
```

To set up postgresql create a user and a database and then add user credentials and database name to settings.py like this.
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'YOUR_DATABASE_NAME',
        'USER': 'YOUR_USERNAME',
        'PASSWORD': 'YOUR_PASSWORD'
    }
}
```

Admin can create and manage blog posts through admin module. To access admin module you must create a superuser (Your postgresql server must be running for the following commands).

To create superuser run this command:
```
$ python manage.py createsuperuser
```

and then enter your username, email and password.

To make migrations :
```
$ python manage.py migrate
```
To run server :
```
$ python manage.py runserver
```

After starting server go to your web browser and visit http://localhost:8000/blog and for admin module visit http://localhost:8000/admin and login using superuser credentials.

This app uses [django-taggit](https://django-taggit.readthedocs.io) to add tags to blog posts and [bootstrap 4](https://getbootstrap.com) for styling. 