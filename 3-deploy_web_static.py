#!/usr/bin/python3
"""Fabric script to create and distribute an archive to web servers"""
from fabric.api import *
import os
from datetime import datetime

env.user = 'ubuntu'
env.hosts = ['100.26.228.117', '107.22.146.104']


def do_pack():
    """Create a compressed tarball of web_static contents"""
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    local("mkdir -p versions")
    file_path = "versions/web_static_{}.tgz".format(now)
    command = "tar -czvf {} web_static".format(file_path)
    result = local(command)
    if result.succeeded:
        return file_path
    return None


def do_deploy(archive_path):
    """Deploys archive to web servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        name = os.path.basename(archive_path)
        wname = name.split(".")[0]
        releases_path = "/data/web_static/releases/{}/".format(wname)
        tmp_path = "/tmp/{}".format(name)

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(releases_path))
        run("tar -xzf {} -C {}".format(tmp_path, releases_path))
        run("rm {}".format(tmp_path))
        run("mv {}web_static/* {}".format(releases_path, releases_path))
        run("rm -rf {}web_static".format(releases_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(releases_path))
        return True
    except Exception as e:
        print("Error deploying:", e)
        return False


def deploy():
    """Full deployment process"""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
