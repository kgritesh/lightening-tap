# -*- coding: utf-8 -*-
from sanic import Blueprint

from lndtap.config import config
from lndtap.util.btcutils import BTCAmount

faucet_bp = Blueprint("faucet", url_prefix="/api/{}".format(config.API_VERSION))


@faucet_bp.get("/stats")
def stats(request):
    context = request["context"]
    lnrpc = context["lnrpc"]
    wallet_balance = lnrpc.wallet_balance()
    node_info = lnrpc.get_info()
    return {
        "total_balance": BTCAmount(wallet_balance["confirmed_ba"]).btc,
        "channels": node_info["num_active_channels"],
        "pending_channels": node_info["num_pending_channels"],
        "network": config.FAUCET_NETWORK,
        "node": "{pubkey}:{ip}".format(
            pubkey=node_info["identity_pubkey"], ip=config.LND_NODE_IP
        ),
    }
