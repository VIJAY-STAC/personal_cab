
#!/usr/bin/bash

sudo systemctl daemon-reload
sudo rm -f /etc/nginx/sites-enabled/blog
sudo rm -f /etc/nginx/sites-enabled/blog2

sudo cp /home/ubuntu/blogrepo/nginx/nginx.conf /etc/nginx/sites-available/blog
sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled/
#sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled
#sudo nginx -t
sudo gpasswd -a www-data ubuntu
echo "Restarting nginx..."
sudo systemctl restart nginx

echo "Restarted nginx..."