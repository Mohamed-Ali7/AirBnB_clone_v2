#!/usr/bin/python3

"""This module contains do_pack() and do_deploy() functions"""

from fabric.api import *
import os


env.hosts = ['54.208.120.231', '54.89.61.73']


def do_deploy(archive_path):
    """Distributes an archive to a web servers"""

    try:
        if not os.path.exists(archive_path):
            return False

        archive_name = archive_path.split("/")[-1]
        web_path = "/data/web_static/releases/{}"\
            .format(archive_name.split('.')[0])

        put(archive_path, "/tmp/")

        run("mkdir -p {}".format(web_path))

        run("tar -xzf /tmp/{} -C {}/".format(archive_name, web_path))
        run("rm /tmp/{}".format(archive_name))

        run("mv {}/web_static/* {}".format(web_path, web_path))

        run("rm -rf {}/web_static".format(web_path))

        run("rm -rf /data/web_static/current")
        run("ln -sf {}/ /data/web_static/current".format(web_path))
        return True
    except:
        return False
