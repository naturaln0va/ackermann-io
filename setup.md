
Via: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04

* sudo apt update
* sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools git nginx python3-venv

* git clone {repo}

* sudo ls /etc/systemd/system
* sudo rm /etc/systemd/system/acker.service
* sudo nano /etc/systemd/system/acker.service

``` FILE CONTENTS
[Unit]
Description=Gunicorn instance to serve ackermann.io
After=network.target

[Service]
User=ryan
Group=www-data
WorkingDirectory=/home/ryan/ackermann
Environment="PATH=/home/ryan/ackermann/venv/bin"
ExecStart=/home/ryan/ackermann/venv/bin/gunicorn --workers 3 --bind unix:acker.sock -m 007 app:app
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

* sudo systemctl start acker
* sudo systemctl enable acker
* sudo systemctl status acker

Allow NGINX `sudo ufw allow 'Nginx Full'`
Check the firewall config `sudo ufw status`

* sudo rm /etc/nginx/sites-available/default
* sudo nano /etc/nginx/sites-available/default

``` FILE CONTENTS
server {
    server_name www.ackermann.io;
    return 301 $scheme://ackermann.io$request_uri;
}
server {
  listen 80;
  server_name ackermann.io;
  
  location / {
    include proxy_params;
    proxy_pass http://unix:/home/ryan/ackermann/acker.sock;
  }
}
```

sudo systemctl restart nginx

***

### Certbot configuration

sudo apt install python3-certbot-nginx

sudo certbot --nginx -d ackermann.io -d www.ackermann.io