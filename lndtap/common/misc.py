# -*- coding: utf-8 -*-
import os

from sanic import Blueprint

from lndtap.util import utils


def find_blueprints(project_dir, app_dir):
    """
    Find all Blueprint instances found in all modules for the specified package.
    """
    for view_file in utils.find_matching_files(app_dir, "blueprint.py"):
        rel_path = os.path.relpath(view_file, project_dir)
        view_module = utils.import_module_from_path(rel_path)
        for item_name in dir(view_module):
            item = getattr(view_module, item_name)
            if isinstance(item, Blueprint):
                yield item
