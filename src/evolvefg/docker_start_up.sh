#!/bin/bash

# Collect static files
#echo "Collect static files"
#python manage.py collectstatic --noinput

jq -r .capif_host=\"$CAPIF_HOSTNAME\" capif_registration.json >> tmp.json && mv tmp.json capif_registration.json
jq -r .capif_http_port=\"$CAPIF_PORT_HTTP\" capif_registration.json >> tmp.json && mv tmp.json capif_registration.json
jq -r .capif_https_port=\"$CAPIF_PORT_HTTPS\" capif_registration.json >> tmp.json && mv tmp.json capif_registration.json
jq -r .capif_callback_url=\"$CALLBACK_ADDRESS\" capif_registration.json >> tmp.json && mv tmp.json capif_registration.json
evolved5g register-and-onboard-to-capif --config_file_full_path="/code/capif_registration.json" --environment="development"

# Make migrations
echo "Making migrations"
python3 manage.py makemigrations --noinput
echo "Making migrations for custom apps..."
python3 manage.py makemigrations netapp_endpoint

# Apply database migrations
echo "Apply database migrations"
python3 manage.py migrate

echo "Creating superUser..."
echo "from netapp_endpoint.models import User; User.objects.create_superuser('admin','admin', 'admin@gmail.com','admin','admin')" | python manage.py shell

echo "Populating Cells of Fogus scenario..."
python manage.py loaddata cells_fogus_scenario.json

# Start server
echo "Starting server"
python3 manage.py runserver 0.0.0.0:8000