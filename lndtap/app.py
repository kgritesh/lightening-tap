# -*- coding: utf-8 -*-
from sanic import Sanic
from sanic import response
from sanic.exceptions import NotFound, ServerError, SanicException

from lndtap.common.misc import find_blueprints
from lndtap.common.middlewares import context_middleware
from lndtap.config import config


def create_app():
    log_config = config.load_config_sync()
    app = Sanic(name="riemann", load_env=False, log_config=log_config)
    app.config.from_object(config)
    register_middlewares(app)
    register_routes(app)
    register_blueprints(app)
    register_exception_handler(app)
    return app


def register_blueprints(app):
    for bp in find_blueprints(config.PROJECT_ROOT, config.APP_DIR):
        app.blueprint(bp)


def version(request):
    return response.json({"version": config.VERSION, "api_version": config.API_VERSION})


def register_routes(app):
    app.add_route(version, "/api/{}/version".format(config.API_VERSION))


def register_middlewares(app):
    app.register_middleware(context_middleware, attach_to="request")


def register_exception_handler(app):

    @app.exception(NotFound)
    def not_found(request, exception):
        return response.json(
            {"error": "Page not found: {}".format(request.url)}, status=404
        )

    @app.exception(SanicException)
    def handle_sanic_exception(request, exception):
        logger = request["context"]["logger"]
        logger.exception(str(exception), exc_info=exception)
        return response.json({"error": str(exception)}, status=exception.status_code)

    @app.exception(Exception)
    def unhandled_exception(request, exception):
        logger = request["context"]["logger"]
        logger.exception(
            "Unhandled Server Error: {}".format(exception), exc_info=exception
        )
        return response.json({"error": "Internal Server Error"}, status=500)
