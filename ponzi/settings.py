from django.conf import settings

PONZI_WALLET_HOST = getattr(settings, 'PONZI_WALLET_HOST', 'localhost')
PONZI_WALLET_PORT = getattr(settings, 'PONZI_WALLET_PORT', 8332)
PONZI_WALLET_RPC_USER = getattr(settings, 'PONZI_WALLET_RPC_USER', "bitcoinrpc")
PONZI_WALLET_RPC_PASSWORD = getattr(settings, 'PONZI_WALLET_RPC_PASSWORD',  ("password",
PONZI_WALLET_PASSPHRASE = getattr(settings, 'PONZI_WALLET_PASSPHRASE', "password")
PONZI_USER_REWARD = getattr(settings, 'PONZI_USER_REWARD', 30)
PONZI_ADMIN_REWARD = getattr(settings, 'PONZI_ADMIN_REWARD', 5) 
PONZI_UPPER_LIMIT = getattr(settings, 'PONZI_UPPER_LIMIT', 1.0) 
PONZI_LOWER_LIMIT = getattr(settings, 'PONZI_LOWER_LIMIT', 0.01) 
PONZI_FEE_BUFFER = getattr(settings, 'PONZI_FEE_BUFFER', 0.0003) 

