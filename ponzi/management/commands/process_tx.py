from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from ponzi.models import Tx, AddressPair, RewardPeriod
from ponzi.utils import get_server
from ponzi.settings import *

import bitcoinrpc
from datetime import datetime


class Command(BaseCommand):
    help = 'Processing incoming and outgoing transactions, triggered by walletnotify'

    def handle(self, txid, *args, **options):

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
                tx.date=datetime.fromtimestamp(transaction.time, tz=timezone.get_default_timezone())
                tx.confirmed = transaction.confirmations > 0
                if d['amount'] < 0:
                    tx.donation = False
                else:
                    tx.donation = not PONZI_LOWER_LIMIT < d['amount'] < PONZI_UPPER_LIMIT
                    
                tx.isreward = isreward
                tx.save()
                
        RewardPeriod.objects.all().latest().do_rewards()

