from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from ponzi.models import Tx


class Command(BaseCommand):
    help = '''Processing incoming and outgoing transactions,
              triggered by walletnotify'''

    def handle(self, txid, *args, **options):

        Tx.process_tx(txid)
