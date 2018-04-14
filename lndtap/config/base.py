# -*- coding: utf-8 -*-

import os
from os.path import abspath, join, dirname

os_env = os.environ.get


def _get_version(project_root):
    with open(join(project_root, "VERSION")) as fd:
        return fd.read().strip()


class Config:
    """
    Base class for config for all environments
    """

    # app paths
    PROJECT_ROOT = abspath(dirname(dirname(os.path.dirname(__file__))))

    APP_DIR = join(PROJECT_ROOT, "lndtap")

    PROTOS_ROOT = join(APP_DIR, "lnrpc", "proto")

    # DEBUG
    DEBUG = os_env("DEBUG", "1") == "1"

    PROJECT_ENV = os_env("PROJECT_ENV", "dev")

    # VERSION
    API_VERSION = "v1"
    VERSION = _get_version(PROJECT_ROOT)

    # SECRETS
    SECRET_KEY = os_env("APP_SECRET_KEY", "secret-key")

    # DB
    DB_URI = "postgresql://riemann:riemann@localhost/riemann"
