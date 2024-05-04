#!/usr/bin/python3

"""This module contains do_clean() function"""


import os
from fabric.api import *


env.hosts = ['54.208.120.231', '54.89.61.73']


def do_clean(number=0):
    """Deletes out-of-date archives"""
    files = local("ls -1t versions", capture=True)
    file_names = files.split(" ")
    n = int(number)
    if n in (0, 1):
        n = 1
    for i in file_names[n:]:
        local("rm versions/{}".format(i))
    dir_server = run("ls -1t /data/web_static/releases")
    dir_server_names = dir_server.split(" ")
    for i in dir_server_names[n:]:
        if i is 'test':
            continue
        run("rm -rf /data/web_static/releases/{}"
            .format(i))
