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


EXPOSE 8000

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN apk add --update --no-cache gdal-dev gcc g++ postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
      build-base postgresql-dev musl-dev zlib zlib-dev

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

RUN rm -rf /tmp && \
    apk del .tmp-build-deps


ENV PATH="/py/bin:$PATH"



COPY ./app /app
WORKDIR /app
RUN apk add --no-cache netcat-openbsd
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
#CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
