# -*- coding: utf-8 -*-
import fnmatch
import importlib
import os


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
