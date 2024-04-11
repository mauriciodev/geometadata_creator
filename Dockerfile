FROM python:3 AS gmd_creator
EXPOSE 8000
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /app

RUN python manage.py makemigrations &&\
    python manage.py migrate

ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]

#CMD [ "gunicorn","--bind", ":8000", "--workers", "3","pfc2024.wsgi" ]
