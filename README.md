# Shareable
An app for sharing links and files in the secure way.

## Demo
The application is online under the following link
https://shareable-app.herokuapp.com

**Note:** the debug mode is on just for a demo purposes, so that the media files can be easily served without any extra CDN service. In the real production environment the `DEBUG = False` shall be set up in the settings.

## Tech-stack
- Python 3.7.2
- Django 2.2.5
- Django Rest Framework 3.10.3

## Set up
### Preconditions
- Docker
- docker-compose

### Commands

### Run migrations
```
$ docker-compose run app python manage.py migrate
```

### Create a superuser
```
$ docker-compose run app python manage.py createsuperuser
```

## Usage
### Commands

### Run server
```
$ docker-compose up app
```

### Run tests
**Note:** you need to install pipenv's `dev-packages` first (`pipenv install --dev`)
```
$ docker-compose run app python manage.py test
```

## API
Find a [Postman collection](Shareable.postman_collection.json) for the API examples.
