# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

import grpc


from lndtap.lnrpc import rpc_pb2 as ln
from lndtap.lnrpc import rpc_pb2_grpc as lnrpc


class Client:

    def __init__(self, lnd_node, cert, macaroon=None):
        print("Lnd Node", lnd_node)
        cert_creds = grpc.ssl_channel_credentials(cert)
        if macaroon:
            macroon_creds = self.get_macroon_creds(macaroon)
            creds = grpc.composite_channel_credentials(cert_creds, macroon_creds)
        else:
            creds = cert_creds

        channel = grpc.secure_channel(lnd_node, creds)
        os.environ["GRPC_SSL_CIPHER_SUITES"] = "HIGH+ECDSA"
        self.client = lnrpc.LightningStub(channel)

    @staticmethod
    def get_macroon_creds(macaroon):

        def metadata_callback(context, callback):
            # for more info see grpc docs
            callback([("macaroon", macaroon)], None)

        return grpc.metadata_call_credentials(metadata_callback)

    def wallet_balance(self):
        return self.client.WalletBalance(ln.WalletBalanceRequest())

    def get_info(self):
        return self.client.GetInfo(ln.GetInfoRequest())
