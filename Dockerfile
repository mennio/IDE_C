FROM python:3.11.3-slim-bullseye
WORKDIR /app

COPY Pipfile .
COPY Pipfile.lock .

RUN pip install --upgrade pip \
    && pip install pipenv \
    && pipenv install --python /usr/local/bin/python --system

COPY code_builder/ ./code_builder
COPY compiler/ ./compiler
COPY manage.py .
