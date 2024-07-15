# FROM ubuntu:24.04 AS gmd_creator
# EXPOSE 8000
#
# RUN apt update && apt install -y python3 python3-gdal python3-pip
#
# # Copiando os arquivos do app para o diretorio /app
# WORKDIR /app
# COPY ./app/ /app
#
# COPY requirements.txt /app
# RUN pip3 install -r requirements.txt --no-cache-dir --break-system-packages
# ENV PATH="/py/bin:$PATH"
#
# RUN python3 manage.py makemigrations && \
#     python3 manage.py migrate
#
# # ENTRYPOINT ["python3"]
# CMD ["python3","manage.py", "runserver", "0.0.0.0:8000"]
#
# #CMD [ "gunicorn","--bind", ":8000", "--workers", "3","pfc2024.wsgi" ]



FROM python:3.11-alpine3.20
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000


RUN python -m venv /py && \
    apk add --update --no-cache gdal-dev gcc g++ && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt &&\
    rm -rf /tmp
    # adduser \
    #   --disabled-password \
    #   --no-create-home \
    #   django-user

ENV PATH="/py/bin:$PATH"

# USER django-user

