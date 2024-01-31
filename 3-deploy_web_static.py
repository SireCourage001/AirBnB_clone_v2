#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
import os.path
from datetime import datetime
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run

env.hosts = ["52.87.229.242", "52.3.241.114"]


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    the_date = datetime.utcnow()
    wkn_file = "versions/web_static_{}{}{}{}{}{}.tgz".format(the_date.year,
                                                         the_date.month,
                                                         the_date.day,
                                                         the_date.hour,
                                                         the_date.minute,
                                                         the_date.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(wkn_file)).failed is True:
        return None
    return wkn_file


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the wkn_file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if os.path.isfile(archive_path) is False:
        return False
    wkn_file = archive_path.split("/")[-1]
    f_name = wkn_file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(wkn_file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(f_name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(f_name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(wkn_file, f_name)).failed is True:
        return False
    if run("rm /tmp/{}".format(wkn_file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(f_name, f_name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(f_name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(f_name)).failed is True:
        return False
    return True


def deploy():
    """Create and distribute an archive to a web server."""
    wkn_file = do_pack()
    if wkn_file is None:
        return False
    return do_deploy(wkn_file)
