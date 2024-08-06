#!/bin/bash
#sqlite3
#.mode csv
#.import gmd_creator_app/fixtures//gmd_creator_app_metadataformfield.csv gmd_creator_app_metadataformfield
#gmd_creator_app

python ../../manage.py dumpdata core.MetadataFormField core.ProductType > form_fields.json
python ../../manage.py dumpdata core.IndexMap > index_map.json

#python manage.py loaddata core/fixtures/form_fields.json
#python manage.py loaddata core/fixtures/index_map.json
