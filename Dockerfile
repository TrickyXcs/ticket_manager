FROM python:3.11-slim-buster

WORKDIR /usr/src/app/bot

COPY pyproject.toml poetry.lock /usr/src/app/bot/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY . /usr/src/app/bot