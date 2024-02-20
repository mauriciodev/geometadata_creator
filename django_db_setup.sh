#!/bin/bash
#docker exec -it gmd_creator python manage.py collectstatic
docker exec -it gmd_creator python manage.py makemigrations
docker exec -it gmd_creator python manage.py migrate
docker exec -it gmd_creator python manage.py createsuperuser
