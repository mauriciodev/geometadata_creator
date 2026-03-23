# geometadata_creator

## Docker

On the root folder:
`docker-compose up`

The django container mounts a volume to the source code, so that the changes on the code are reloaded by Django. Disable this when deploying for production.

To setup the database, use `./django_db_setup.sh`. The file contains examples of running Django manage commands in the container.


`docker exec -it gmd_creator python manage.py collectstatic`  
`docker exec -it gmd_creator python manage.py makemigrations core xml_handler`  
`docker exec -it gmd_creator python manage.py migrate`  
`docker exec -it gmd_creator python manage.py createsuperuser`  
`docker exec -it gmd_creator python3 manage.py loaddata core/fixtures/form_fields.json core/fixtures/index_map.json`  
