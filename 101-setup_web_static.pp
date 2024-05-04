# Puppet script to install and configure an Nginx server

$alias='\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}'
$after_line='listen \[::\]:80 default_server;'

package { 'nginx':
  ensure          => installed,
  provider        => 'apt',
  install_options => ['-y'],
} ->

file { '/data':
  ensure  => 'directory'
} ->

file { '/data/web_static':
  ensure => 'directory'
} ->

file { '/data/web_static/releases':
  ensure => 'directory'
} ->

file { '/data/web_static/releases/test':
  ensure => 'directory'
} ->

file { '/data/web_static/shared':
  ensure => 'directory'
} ->

file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "Holberton School Puppet\n"
} ->

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test'
} ->

exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/'
} ->

exec { 'add_alias':
  command => "sed -i '/${after_line}/a\ ${alias}' /etc/nginx/sites-available/default",
  path    => '/usr/bin/:/usr/local/bin/:/bin/',
} ->

service { 'nginx':
  ensure => 'running',
}
