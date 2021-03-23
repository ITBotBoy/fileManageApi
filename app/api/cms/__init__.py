"""
    register api to admin blueprint
    ~~~~~~~~~
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from flask import Blueprint


def create_cms():
    cms = Blueprint('cms', __name__)
    from .admin import admin_api
    from .user import user_api
    from .log import log_api
    from .file import file_api
    from .bigfile import bigfile_api
    from .test import test_api
    from .file_group import file_group_api
    admin_api.register(cms)
    user_api.register(cms)
    log_api.register(cms)
    file_api.register(cms)
    bigfile_api.register(cms)
    test_api.register(cms)
    file_group_api.register(cms)
    return cms
