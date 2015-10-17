from django.db import models
from django.utils import timezone
from .utils import get_server
from .settings import *
import bitcoinrpc
from datetime import datetime


class AddressPair(models.Model):
    user_addr = models.CharField(max_length=40, unique=True)
    site_addr = models.CharField(max_length=35, null=True)

    def __str__(self):
        return "User:{0} ___ Site:{1}".format(self.user_addr, self.site_addr)
    
    @property
    def user_addr_unique(self):
        return 'IUSER' + self.user_addr


class RewardPeriod(models.Model):
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'date'

    def __str__(self):
        return self.date.strftime("%B %d, %Y")

    def get_total(self):
        return self.get_received() + self.get_sent()

    def get_received(self):
        return sum([tx.amount for tx in self.tx_set.filter(amount__gt=0,
                                                           donation=False,
                                                           confirmed=True,
                                                           isreward=False)])

    def get_sent(self):
        return sum([tx.amount for tx in self.tx_set.filter(amount__lt=0,
                                                           donation=False)])

    def do_rewards(self):
        for t in self.tx_set.filter(confirmed=True,
                                    rewarded=False,
                                    donation=False,
                                    isreward=False):
            self.reward_next()

    def reward_next(self):
        tx = self.tx_set.filter(confirmed=True,
                                rewarded=False,
                                donation=False,
                                isreward=False).order_by('date')[0]
        if tx.get_reward_threshold()+FEE_BUFFER <= self.get_total():
            server = get_server()
            account = tx.addresspair.user_addr_unique

            try:
                server.walletpassphrase(PONZI_WALLET_PASSPHRASE, 600)
            except bitcoinrpc.exceptions.WalletAlreadyUnlocked:
                pass

            txid = server.sendtoaddress(account, tx.get_reward())
            server.walletlock()
            rawrewardtx = server.gettransaction(txid)
            rewardtx_amount = rawrewardtx.amount + rawrewardtx.fee
            rewardtx, created = Tx.objects.get_or_create(txid=txid,
                                                         addresspair=tx.addresspair,
                                                         amount=rewardtx_amount)
            rewardtx.isreward = True
            rewardtx.rewardperiod = self
            rewardtx.rewardtx = tx
            rewardtx.save()
            tx.rewardtx = rewardtx
            tx.rewarded = True
            tx.save()


class Tx(models.Model):
    txid = models.CharField(max_length=64, blank=True, null=True)
    addresspair = models.ForeignKey(AddressPair)
    rewardperiod = models.ForeignKey(RewardPeriod, null=True)
    rewardtx = models.OneToOneField('Tx', null=True, blank=True)
    isreward = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=16, decimal_places=8)
    date = models.DateTimeField(default=timezone.now)
    confirmed = models.BooleanField(default=False)
    rewarded = models.BooleanField(default=False)
    donation = models.BooleanField(default=False)

    def __str__(self):
        return self.txid

    def get_reward(self):
        percent = (100.0 + PONZI_USER_REWARD) / 100.0
        return round(float(self.amount) * percent, 8)

    def get_reward_threshold(self):
        percent = (100.0 + PONZI_USER_REWARD + PONZI_ADMIN_REWARD) / 100.0
        return round(float(self.amount) * percent, 8)

    @staticmethod
    def process_tx(txid):

        server = get_server()
        transaction = server.gettransaction(txid)

        for d in transaction.details:
            addresspairs = None
            if d['account']:
                print d['account']
                if d['category'] == 'receive':
                    isreward = False
                    addresspairs = AddressPair.objects.filter(user_addr=d['account'][5:])
                    print addresspairs
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
                                                       amount=d['amount'] + fee,
                                                       )
                if d['category'] == 'receive':
                    tx.rewardperiod = RewardPeriod.objects.all().latest()
                tx.date = datetime.fromtimestamp(transaction.time,
                                                 tz=timezone.get_default_timezone())

                tx.confirmed = transaction.confirmations > 0
                if d['amount'] < 0:
                    tx.donation = False
                else:
                    tx.donation = not PONZI_LOWER_LIMIT < d['amount'] < PONZI_UPPER_LIMIT

                tx.isreward = isreward
                tx.save()

        RewardPeriod.objects.all().latest().do_rewards()
