FROM python:3.7.2-alpine3.9

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

RUN apk update && apk add \
      alpine-sdk
RUN pip install pipenv

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pip install -U pipenv
RUN pipenv install --system --verbose

COPY . /app

RUN mkdir -p logs
RUN python src/manage.py collectstatic --noinput
RUN python src/manage.py migrate

RUN adduser -D myuser
USER myuser

WORKDIR /app/src/
CMD gunicorn --bind 0.0.0.0:$PORT wsgi:application
