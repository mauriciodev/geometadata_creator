#!/bin/bash
#docker exec -it gmd_creator python manage.py collectstatic
#docker exec -it gmd_creator python manage.py makemigrations
#docker exec -it gmd_creator python manage.py migrate
#docker exec -it gmd_creator python manage.py createsuperuser
python app/manage.py collectstatic
python app/manage.py makemigrations
python app/manage.py makemigrations gmd_creator_app
python app/manage.py migrate
python app/manage.py createsuperuser
python app/manage.py loaddata app/gmd_creator_app/fixtures/form_fields.json
