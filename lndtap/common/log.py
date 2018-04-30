# -*- coding: utf-8 -*-
import logging

from lndtap.config import config


class RequireDebugFalse(logging.Filter):
    # Taken from django

    def filter(self, record):
        return not config.DEBUG


class RequireDebugTrue(logging.Filter):
    # Taken from django

    def filter(self, record):
        return config.DEBUG
