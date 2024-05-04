# Puppet script to install and configure an Nginx server

exec { 'update':
  command => '/usr/bin/apt-get update',
}
-> package { 'nginx':
ensure          => installed,
provider        => 'apt',
install_options => ['-y'],
}
-> exec {'create test directory':
  command  => 'mkdir -p /data/web_static/releases/test/',
  provider => 'shell',
}
-> exec { 'create shared directory':
command  => 'mkdir -p /data/web_static/shared/',
provider => 'shell',
}
-> file {'/data/web_static/releases/test/index.html':
content => 'Hello World!',
}
-> file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
}
-> exec { 'change owner':
command  => 'chown -hR ubuntu:ubuntu /data/',
provider => shell,
}
-> file_line { 'add_alias':
  ensure => 'present',
  path   => '/etc/nginx/sites-available/default',
  after  => 'listen \[::\]:80 default_server;',
  line   => "\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}",
}
-> service { 'nginx':
  ensure => 'running',
}
