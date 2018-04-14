#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import subprocess

import click

from lndtap.config import config


@click.group()
def cli():
    pass


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
