#!/bin/bash

# Collect static files
#echo "Collect static files"
#python manage.py collectstatic --noinput

# Make migrations
echo "Making migrations"
python3 manage.py makemigrations --noinput
echo "Making migrations for custom apps..."
python3 manage.py makemigrations netapp_endpoint

# Apply database migrations
echo "Apply database migrations"
python3 manage.py migrate

echo "Creating superUser..."
# winpty docker-compose run python manage.py createsuperuser | python manage.py shell
# echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')" | python manage.py shell
echo "from netapp_endpoint.models import User; User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')" | python manage.py shell

# Start server
echo "Starting server"
python3 manage.py runserver 0.0.0.0:8000