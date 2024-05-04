#!/usr/bin/env bash
# script that sets up web servers for the deployment of web_static
apt-get update
apt-get -y install nginx

mkdir -p /data/
mkdir -p /data/web_static/
mkdir -p /data/web_static/releases/
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
echo "Hello World!" > /data/web_static/releases/test/index.html

ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

new="\n\
\tlocation /hbnb_static {\n\
\t\talias /data/web_static/current/;\n\
\t}
"
sed -i "/listen \[::\]:80 default_server;/a\ $new" /etc/nginx/sites-available/default

ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

service nginx restart
