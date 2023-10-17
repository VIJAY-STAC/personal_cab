
#!/usr/bin/bash

sudo systemctl daemon-reload
sudo rm -f /etc/nginx/sites-enabled/cars


sudo cp /home/ubuntu/personal_car/nginx/nginx.conf /etc/nginx/sites-available/cars
sudo ln -s /etc/nginx/sites-available/cars /etc/nginx/sites-enabled/
#sudo ln -s /etc/nginx/sites-available/cars /etc/nginx/sites-enabled
#sudo nginx -t
sudo gpasswd -a www-data ubuntu
echo "Restarting nginx..."
sudo systemctl restart nginx

echo "Restarted nginx..."