# -*- coding: utf-8 -*-
import asyncio
import fnmatch
import functools
import importlib
import os
import socket

import sys


def find_matching_files(path, pattern):
    """
    Find all the files matching given `pattern` recursively in
    the specified `path`
    """
    for root, dirnames, filenames in os.walk(path):

        # Remove hidden directories from walk
        for dr in dirnames:
            if dr.startswith("."):
                dirnames.remove(dr)
        for filename in fnmatch.filter(filenames, pattern):
            yield os.path.join(root, filename)


def import_module_from_path(path, parent_package=None):
    """
    Import a module from specified path
    :param path:
    :param parent_package:
    :return:
    """
    path = os.path.splitext(path)[0]
    if path.endswith("/"):
        path = path[:-1]

    path = path.replace("/", ".")
    return importlib.import_module(path, parent_package)


def get_app_data_dir(app_name):
    app_name = app_name.lstrip(".")
    home = os.path.expanduser("~")

    if sys.platform == "darwin":
        # Mac OSX
        return os.path.join(home, "Library", "Application Support", app_name.title())

    elif sys.platform == "windows":
        app_data = os.environ.get("LOCALAPPDATA", os.environ.get("APPDATA"))
        if app_data:
            return os.path.join(app_data, app_name.title())

    else:
        return os.path.join(home, ".{}".format(app_name[0].lower() + app_name[1:]))


def parse_bool(boolstr):
    return boolstr.lower() in ["t", "true", "1", "y", "yes"]


def get_local_ip():
    return socket.gethostbyname(socket.getfqdn())


def memoize(func):
    cache = {}

    def _wrap_coroutine_storage(key, val):

        async def _wrapper():
            value = await val
            cache[key] = value
            return value

        return _wrapper()

    def _wrap_value_in_coroutine(val):

        async def _wrapper():
            return val

        return _wrapper()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = repr((args, kwargs))
        if key not in cache:
            val = func(*args, **kwargs)
            if asyncio.iscoroutine(val):
                return _wrap_coroutine_storage(key, val)

            return val

        else:
            val = cache[key]
            if asyncio.iscoroutinefunction(func):
                return _wrap_value_in_coroutine(val)

            return val

    return wrapper
