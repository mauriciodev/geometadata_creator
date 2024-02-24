#!/bin/bash
#docker exec -it gmd_creator python manage.py collectstatic
#docker exec -it gmd_creator python manage.py makemigrations
#docker exec -it gmd_creator python manage.py migrate
#docker exec -it gmd_creator python manage.py createsuperuser
python manage.py collectstatic
python manage.py makemigrations
python manage.py makemigrations gmd_creator_app
python manage.py migrate
python manage.py createsuperuser
