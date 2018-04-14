# -*- coding: utf-8 -*-
from sanic import Sanic
from sanic import response

from lndtap.common.misc import find_blueprints
from lndtap.config import config


def create_app():
    app = Sanic(name="riemann", load_env=False)
    app.config.from_object(config)
    register_routes(app)
    register_blueprints(app)
    return app


def register_blueprints(app):
    for bp in find_blueprints(config.PROJECT_ROOT, config.APP_DIR):
        app.register_blueprint(bp)


def version(request):
    return response.json({"version": config.VERSION, "api_version": config.API_VERSION})


def register_routes(app):
    app.add_route(version, "/api/{}/version".format(config.API_VERSION))
