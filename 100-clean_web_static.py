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

    try:
        number = int(number)
        if number < 1:
            number = 1
        with cd('/data/web_static/releases'):
            archives = run('ls -t').split()
            for archive in archives[number:]:
                run('rm -rf {}'.format(archive))
        with lcd('versions'):
            archives = local('ls -t', capture=True).split()
            for archive in archives[number:]:
                local('rm -rf {}'.format(archive))
    except:
        return False
