#!/usr/bin/python3

"""This module contains do_clean() function"""


import os
from fabric.api import *


env.hosts = ['54.208.120.231', '54.89.61.73']


def do_clean(number=0):
    """Deletes out-dated archives.

    Args:
        number (int): The number of archives to keep.
    """

    number = int(number)

    if number == 0:
        number = 1

    local_archives = local("ls -t versions || true", capture=True).split()
    for archive in local_archives[number:]:
        local("rm -f versions/{}".format(archive))

    remote_archives = run("ls -t /data/web_static/releases/ | grep web_stat*")
    remote_archives = remote_archives.split()
    for archive in remote_archives[number:]:
        sudo("rm -rf /data/web_static/releases/{}".format(archive))
