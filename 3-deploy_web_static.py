#!/usr/bin/python3

"""This module contains do_pack() and do_deploy() functions"""

from fabric.api import *
from datetime import datetime
import os


env.hosts = ['54.208.120.231', '54.89.61.73']


def do_pack():
    """Generates a .tgz archive from the contents of the web_static"""

    try:
        now = datetime.now().strftime('%Y%m%d%H%M%S')
        archive_path = "versions/web_static_{}.tgz".format(now)
        local("mkdir -p versions")
        local("tar -czvf {} web_static".format(archive_path))
        return archive_path
    except:
        return None


def do_deploy(archive_path):
    """Distributes an archive to a web servers"""

    try:
        if not os.path.exists(archive_path):
            return False
        put(archive_path, "/tmp/")

        archive_name = archive_path.split("/")[-1]
        web_path = f"/data/web_static/releases/{archive_name.split('.')[0]}"

        run(f"mkdir -p {web_path}")

        run(f"tar -xzf /tmp/{archive_name} -C {web_path}")
        run(f"rm /tmp/{archive_name}")

        run(f"mv {web_path}/web_static/* {web_path}")

        run(f"rm -rf {web_path}/web_static")

        run(f"rm -rf /data/web_static/current")
        run(f"ln -s {web_path} /data/web_static/current")

        return True
    except:
        return False


def deploy():
    """Creates and distributes an archive to a web servers"""

    if not hasattr(deploy, 'archive_path'):
        deploy.archive_path = do_pack()
    if not deploy.archive_path:
        return False

    return do_deploy(deploy.archive_path)
