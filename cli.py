#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import subprocess

import click
import hupper

from lndtap.app import create_app
from lndtap.config import config


@click.group()
def cli():
    pass


def run_app(host, port):
    app = create_app()
    app.run(host=host, port=port)


@cli.command(short_help="Start Development Server with autoreloading capability")
@click.option("--host", default="0.0.0.0", help="Host address to bind to")
@click.option("--port", default=7000, help="Port to bind to")
@click.option("--no-reload", default=False, help="Disable reloading")
def runserver(host, port, no_reload=False):
    if no_reload:
        run_app(host, port)

    else:
        hupper.start_reloader("cli.run_app", worker_kwargs={"host": host, "port": port})


@cli.command(
    short_help="Compile the proto file and create client stub for `lnd` rpc calls"
)
def generate_protos():
    """
    Compile the proto file and create client stub for `lnd` rpc calls
    """
    python_out = os.path.join(config.APP_DIR, "lnrpc")
    proto_include = "{}:{}".format(
        os.path.join(config.PROTOS_ROOT, "googleapis"), config.PROTOS_ROOT
    )
    proto_file = "rpc.proto"
    subprocess.call(
        [
            "pipenv",
            "run",
            "python",
            "-m",
            "grpc_tools.protoc",
            "-I",
            proto_include,
            "--python_out",
            python_out,
            "--grpc_python_out",
            python_out,
            proto_file,
        ]
    )


if __name__ == "__main__":
    cli()
