#!/bin/bash
#docker exec -it gmd_creator python manage.py collectstatic
#docker exec -it gmd_creator python manage.py makemigrations
#docker exec -it gmd_creator python manage.py migrate
#docker exec -it gmd_creator python manage.py createsuperuser
python app/manage.py collectstatic
python app/manage.py makemigrations
python app/manage.py makemigrations core
python app/manage.py migrate
python app/manage.py createsuperuser

docker compose run --rm gmd_creator sh -c "python3 manage.py loaddata core/fixtures/form_fields.json core/fixtures/index_map.json"


