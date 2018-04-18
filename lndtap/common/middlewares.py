# -*- coding: utf-8 -*-

from lndtap.config import config
from lndtap.lnrpc.client import Client


async def context_middleware(request):
    cert = await config.read_lnd_cert()
    macaroon = await config.read_macaroon() if config.LND_MACROON_ENABLED else None

    request["context"] = {
        "config": config, "lnrpc": Client(config.LND_NODE, cert, macaroon=macaroon)
    }
