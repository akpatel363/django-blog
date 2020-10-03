# Django Blog

A blog made using django 3, markdown and postgresql.

Other libraries like django-crispy-forms and django-taggit are used for styling and tagging posts respectively.

Install dependencies :

```
$ pip install -r requirements.txt
```

To set up postgresql create a user and a database and then add user credentials and database name in settings.py like this.

```python
DATABASES['default'] = dj_database_url.config(default="postgres://USERNAME:PASSWORD@localhost:5432/DATABASE_NAME")
```

Admin can create and manage blog posts through admin module. To access admin module you must create a superuser (Your postgresql server must be running for the following commands to work).

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

After starting server go to your web browser and visit http://localhost:8000 and for admin module visit http://localhost:8000/admin and login using superuser credentials.

This app uses [bootstrap 4](https://getbootstrap.com) for styling.
