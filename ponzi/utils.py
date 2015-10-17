import bitcoinrpc as btc
from .settings import *


def get_server():
    return btc.connect_to_remote(PONZI_WALLET_RPC_USER,
                                 PONZI_WALLET_RPC_PASSWORD,
                                 host=PONZI_WALLET_HOST,
                                 port=PONZI_WALLET_PORT,
                                 use_https=PONZI_WALLET_USE_HTTPS
                                 )
