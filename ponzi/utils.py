import bitcoinrpc as btc
from django.utils import timezone
from .settings import *
from .models import Tx, AddressPair, RewardPeriod
import bitcoinrpc
from datetime import datetime


def get_server():
    return btc.connect_to_remote(PONZI_WALLET_RPC_USER,
                                 PONZI_WALLET_RPC_PASSWORD,
                                 PONZI_WALLET_HOST,
                                 PONZI_WALLET_PORT,
                                 )

def process_tx(txid):

    server = get_server()
    transaction = server.gettransaction(txid)

    for d in transaction.details:
        if d['category'] == 'receive':
            isreward = False
            addresspairs = AddressPair.objects.filter(user_addr=d['account'])
        elif d['category'] == 'send':
            isreward = True
            addresspairs = AddressPair.objects.filter(user_addr=d['address'])


        if addresspairs:
            addresspair = addresspairs[0]
            fee = 0
            if hasattr(transaction, 'fee'):
                fee = transaction.fee
            tx, created = Tx.objects.get_or_create(txid=transaction.txid,
                                                   addresspair=addresspair,
                                                   amount = d['amount'] + fee,
                                                   )
            if d['category'] == 'receive':
                tx.rewardperiod=RewardPeriod.objects.all().latest()
            tx.date=datetime.fromtimestamp(transaction.time,
                                           tz=timezone.get_default_timezone())

            tx.confirmed = transaction.confirmations > 0
            if d['amount'] < 0:
                tx.donation = False
            else:
                tx.donation = not PONZI_LOWER_LIMIT < d['amount'] < PONZI_UPPER_LIMIT
                
            tx.isreward = isreward
            tx.save()
            
    RewardPeriod.objects.all().latest().do_rewards()

