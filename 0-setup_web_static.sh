#!/usr/bin/env bash
# This script sets up a web servers for the deployment of web_static

apt-get update
apt-get -y install nginx

mkdir -p /data/web_static/releases/test/
mkdir /data/web_static/shared/
echo "Hello World!" > /data/web_static/releases/test/index.html
ln -s /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu:ubuntu /data/

sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default

ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

service nginx restart
