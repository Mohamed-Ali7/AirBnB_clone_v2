#!/usr/bin/python3

"""This module contains do_pack() function"""

from fabric.api import *
from datetime import datetime


def do_pack():
    """Generates a .tgz archive from the contents of the web_static"""

    local("mkdir -p versions")

    now = datetime.now()
    archive_name = f"web_static_{now.strftime('%Y%m%d%H%M%S')}.tgz"

    result = local(f"tar -czvf versions/{archive_name} web_static")

    if result.succeeded:
        return f"versions/{archive_name}"
