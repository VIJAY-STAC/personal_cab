#!/bin/bash

# Change to the correct directory where your application code is located
cd /home/ubuntu/
source /env/bin/activate

cd /personal_car

# Update settings.py file
sed -i 's/\[]/\["13.232.225.109"]/' cars/settings.py

# Print the current working directory for debugging
pwd

# Start the application commands
echo "Starting the app"
python3 manage.py migrate 
echo "Migrations done"
python3 manage.py makemigrations     
python3 manage.py collectstatic
sudo service gunicorn restart
sudo service nginx restart
