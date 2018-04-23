# -*- coding: utf-8 -*-
from sanic import Blueprint
from sanic import response
from sanic.exceptions import InvalidUsage

from lndtap.config import config
from lndtap.util.btcutils import BTCAmount
from google.protobuf.json_format import MessageToJson

from lndtap.util.utils import proto_to_dict

faucet_bp = Blueprint("faucet", url_prefix="/api/{}/faucet".format(config.API_VERSION))


@faucet_bp.get("/stats")
def stats(request):
    context = request["context"]
    lnrpc = context["lnrpc"]
    node_info = lnrpc.get_info()
    wallet_balance = lnrpc.wallet_balance()

    return response.json(
        {
            "total_balance": BTCAmount(wallet_balance.confirmed_balance).btc,
            "channels": node_info.num_active_channels,
            "pending_channels": node_info.num_pending_channels,
            "network": config.FAUCET_NETWORK,
            "node": "{pubkey}@{ip}".format(
                pubkey=node_info.identity_pubkey, ip=config.LND_NODE_IP
            ),
        }
    )


@faucet_bp.post("/connect-peer")
def connect_peer(request):
    context = request["context"]
    lnrpc = context["lnrpc"]
    pubkey = request.json["pubkey"]
    host = request.json["host"]
    lnrpc.connect_peer(pubkey, host)
    peers = lnrpc.list_peers()
    return response.json(proto_to_dict(peers))


@faucet_bp.get("/connections")
def get_peers(request):
    lnrpc = request["context"]["lnrpc"]
    peers = lnrpc.list_peers()
    return response.json({"peers": [proto_to_dict(peer) for peer in peers]})


def channel_exists_with_node(lnrpc, pubkey):
    channel_list = lnrpc.list_open_channels()
    return any(chan.remote_pubkey == pubkey for chan in channel_list)


def connection_exists_with_node(lnrpc, pubkey):
    peer_list = lnrpc.list_peers()
    return any(peer.pub_key == pubkey for peer in peer_list)


@faucet_bp.post("/open-channel")
def open_channel(request):
    context = request["context"]
    lnrpc = context["lnrpc"]
    pubkey = request.json["pubkey"]
    host = request.json["host"]
    channel_amount = int(request.json["channel_amount"])
    initial_balance = int(request.json["initial_balance"])
    if channel_exists_with_node(lnrpc, pubkey):
        raise InvalidUsage("An existing channel exists between the node and the faucet")

    if not connection_exists_with_node(lnrpc, pubkey):
        print("Connecting Peer")
        lnrpc.connect_peer(pubkey, host)

    for resp in lnrpc.open_channel(
        node_pubkey=bytes.fromhex(pubkey),
        node_pubkey_string=pubkey,
        local_funding_amount=channel_amount,
        push_sat=initial_balance,
    ):

        return response.json({"funding_tx_id": resp.chan_pending.txid})
