FROM python:3.7.2-alpine3.9

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

RUN pip install pipenv
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
:
RUN pip install -U pipenv
RUN pipenv install --system --verbose

COPY . /app
