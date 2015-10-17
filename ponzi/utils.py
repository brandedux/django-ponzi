import bitcoinrpc as btc
from .settings import *


def get_server():
    return btc.connect_to_remote(PONZI_WALLET_RPC_USER,
                                 PONZI_WALLET_RPC_PASSWORD,
                                 PONZI_WALLET_HOST,
                                 PONZI_WALLET_PORT,
                                 )
