from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from ponzi.tasks import new_rewardperiod


class Command(BaseCommand):
    help = 'Processing incoming and outgoing transactions, triggered by walletnotify'

    def handle(self, *args, **options):

        new_rewardperiod()

