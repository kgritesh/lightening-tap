# -*- coding: utf-8 -*-
from .base import Config


class ProdConfig(Config):
    PROJECT_ENV = "prod"
