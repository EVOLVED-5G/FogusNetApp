#!/bin/bash

# Collect static files
#echo "Collect static files"
#python manage.py collectstatic --noinput

# Make migrations
echo "Making migrations"
python manage.py makemigrations --noinput
echo "Making migrations for custom apps..."
python manage.py makemigrations netapp_endpoint

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

echo "Creating superUser..."
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')" | python manage.py shell

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000 
