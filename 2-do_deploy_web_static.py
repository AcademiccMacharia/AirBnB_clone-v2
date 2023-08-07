#!/usr/bin/python3
"""Distributes an archive to my web servers"""
from fabric.api import *
import os

env.hosts = ['100.26.228.117', '107.22.146.104']
env.user = "ubuntu"


def do_deploy(archive_path):
    """Distributes an archive to the web servers and deploys it."""

    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")

        archive_filename = os.path.basename(archive_path)
        folder_name = "/data/web_static/releases/{}".format(
            archive_filename.replace(".tgz", "").replace(".tar.gz", ""))
        run("mkdir -p {}".format(folder_name))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, folder_name))
        run("rm /tmp/{}".format(archive_filename))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_name))

        print("New Version deployed!")
        return True

    except Exception as e:
        print("Error deploying:", e)
        return False
