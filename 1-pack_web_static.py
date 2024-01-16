#!/usr/bin/python3
# Fabfile to generates a .tgz archive from the contents of web_static.
import os.path
from datetime import datetime
from fabric.api import local


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    the_date = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(the_date.year,
                                                         the_date.month,
                                                         the_date.day,
                                                         the_date.hour,
                                                         the_date.minute,
                                                         the_date.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file
