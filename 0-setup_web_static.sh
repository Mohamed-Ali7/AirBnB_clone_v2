#!/usr/bin/env bash
# This script sets up a web servers for the deployment of web_static

apt-get update
apt-get -y install nginx

mkdir -p /data/web_static/releases/test/
mkdir /data/web_static/shared/
echo "Hello World!" > /data/web_static/releases/test/index.html
ln -s /data/web_static/releases/test/ /data/web_static/current

chown -hR ubuntu:ubuntu /data/

new="\n\
\tlocation /hbnb_static {\n\
\t\talias /data/web_static/current/;\n\
\t}
"
sed -i "/listen \[::\]:80 default_server;/a\ $new" /etc/nginx/sites-available/default

service nginx restart
