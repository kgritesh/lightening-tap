# -*- coding: utf-8 -*-


class BTCAmount(object):

    CONVERSION_FRACTIONS = {
        "btc": float(10 ** -8), "mbtc": float(10 ** -5), "ubtc": float(10 ** -2)
    }

    FRACTION = float(10 ** -8)

    def __init__(self, amount):
        """
        :param amount: amount in satoshi
        """
        self.amount = int(amount)

    @property
    def satoshi(self):
        return self.amount

    @property
    def btc(self):
        return float(self.amount) * self.CONVERSION_FRACTIONS["btc"]

    @property
    def mbtc(self):
        return float(self.amount) * self.CONVERSION_FRACTIONS["mbtc"]

    @property
    def ubtc(self):
        return float(self.amount) * self.CONVERSION_FRACTIONS["ubtc"]
