# -*- coding: utf-8 -*-
import codecs
import os
from os.path import abspath, join, dirname

import sys

import aiofiles
import yaml
from pymacaroons import Macaroon, Verifier


from lndtap.util import utils
from lndtap.util.utils import parse_bool, get_local_ip, memoize

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

    LOG_CONFIG = join(APP_DIR, "config", "log.yaml")

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

    # LND
    LND_ROOT = os_env("LND_ROOT", utils.get_app_data_dir("lnd"))

    LND_TLS_CERT_PATH = os_env("LND_TLS_CERT_PATH", os.path.join(LND_ROOT, "tls.cert"))

    LND_MACROON_ENABLED = parse_bool(os_env("LND_MACROON_ENABLED", "True"))

    LND_MACAROON_PATH = os_env(
        "LND_MACROONS_PATH", os.path.join(LND_ROOT, "admin.macaroon")
    )

    LND_NODE = os_env("LND_NODE", "127.0.0.1:10001")

    LND_NODE_IP = os_env("LND_NODE_IP", get_local_ip())

    LND_WALLET_PASS = "6tiHYnIdVdg6C5CH"

    # MISC
    FAUCET_NETWORK = os_env("FAUCET_NETWORK", "bitcoin")

    @classmethod
    @memoize
    async def read_lnd_cert(cls):
        async with aiofiles.open(cls.LND_TLS_CERT_PATH, mode="rb") as certfd:
            return await certfd.read()

    @classmethod
    @memoize
    async def read_macaroon(cls):
        async with aiofiles.open(cls.LND_MACAROON_PATH, mode="rb") as macfd:
            mac_bytes = await macfd.read()
            return codecs.encode(mac_bytes, "hex")

    @classmethod
    @memoize
    async def load_config(cls):
        async with aiofiles.open(cls.LOG_CONFIG, mode="r") as certfd:
            return yaml.load(await certfd.read())

    @classmethod
    @memoize
    def load_config_sync(cls):
        with open(cls.LOG_CONFIG, mode="r") as fd:
            return yaml.load(fd.read())
