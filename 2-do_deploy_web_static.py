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
        web_path = f"/data/web_static/releases/{archive_name.split('.')[0]}"

        put(archive_path, "/tmp/")

        run(f"mkdir -p {web_path}")

        run(f"tar -xzf /tmp/{archive_name} -C {web_path}")
        run(f"rm /tmp/{archive_name}")

        run(f"mv {web_path}/web_static/* {web_path}")

        run(f"rm -rf {web_path}/web_static")

        run(f"rm -rf /data/web_static/current")
        run(f"ln -sf {web_path} /data/web_static/current")
        run(f"touch /data/web_static/current/my_index.html")
        print("New version deployed!")
        return True
    except:
        return False
