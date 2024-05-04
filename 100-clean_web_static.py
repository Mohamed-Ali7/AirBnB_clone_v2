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

    local_archives = local("ls -t versions", capture=True).split()
    for archive in local_archives[number:]:
        local(f"rm versions/{archive}")

    unknown_files = run("ls /data/web_static/releases/ | grep -v web_static*", warn_only=True)
    if unknown_files:
        unknown_files = unknown_files.split()
    for file in unknown_files:
        run(f"rm -rf /data/web_static/releases/{file}")

    remote_archives = run("ls -t /data/web_static/releases | grep web_static*")
    remote_archives = remote_archives.split()
    for archive in remote_archives[number:]:
        if archive.startswith("web_static_"):
            run(f"rm -rf /data/web_static/releases/{archive}")
