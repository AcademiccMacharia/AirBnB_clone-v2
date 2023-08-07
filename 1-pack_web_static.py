#!/usr/bin/python3
""" Function that compress a folder """
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""

    if not os.path.exists("versions"):
        os.makedirs("versions")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(timestamp)

    try:
        local("tar -czvf versions/{} web_static".format(archive_name))
        return "versions/{}".format(archive_name)
    except Exception as e:
        print("Error creating archive:", e)
        return None
