#!/usr/bin/env bash
# This script sets up a web servers for the deployment of web_static

#Create the folder /data/ if it doesn’t already exist
#Create the folder /data/web_static/ if it doesn’t already exist
#Create the folder /data/web_static/releases/ if it doesn’t already exist
#Create the folder /data/web_static/shared/ if it doesn’t already exist
#Create the folder /data/web_static/releases/test/ if it doesn’t already exist
#Create a fake HTML file /data/web_static/releases/test/index.html (with simple content, to test your Nginx configuration)
#Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder. If the symbolic link already exists, it should be deleted and recreated every time the script is ran.
#Give ownership of the /data/ folder to the ubuntu user AND group (you can assume this user and group exist). This should be recursive; everything inside should be created/owned by this user/group.
#Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static (ex: https://mydomainname.tech/hbnb_static). Don’t forget to restart Nginx after updating the configuration:
#Use alias inside your Nginx configuration

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
sed -i "#listen \[::\]:80 default_server;#a\ $new#" /etc/nginx/sites-available/default

service nginx restart
