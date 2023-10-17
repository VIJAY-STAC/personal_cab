#!/bin/bash

# Activate the virtual environment (change to your virtual environment path)
pwd
echo "hello1 "
source /home/ubuntu/env/bin/activate
echo "hello2 "
pwd
# Change to the directory where your Django project is located
cd /home/ubuntu/personal_car

# Update the settings.py file
sed -i 's/\[]/\["13.232.225.109"]/' cars/settings.py

# Print the current working directory for debugging
pwd

# Start the application commands
echo "Starting the app"
python manage.py migrate 
echo "Migrations done"
python manage.py makemigrations
python manage.py collectstatic

# Restart services
sudo service gunicorn restart
sudo service nginx restart
