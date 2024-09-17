# The builder image, used to build the virtual environment
FROM python:3.11-alpine3.20

RUN pip install poetry==1.3.2

RUN python -m venv /py

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    VIRTUAL_ENV=/py \
    PATH="py/bin:$PATH"

COPY ./app /app
WORKDIR /app
EXPOSE 8000

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN apk add --update --no-cache gdal-dev gcc g++ && \
    poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR


ENV PATH="/py/bin:$PATH"
