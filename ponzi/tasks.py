from __future__ import absolute_import

from celery import shared_task

from .models import RewardPeriod

@shared_task
def new_rewardperiod():
    old = RewardPeriod.objects.all().latest()
    new = RewardPeriod.objects.create()
    assert new.pk == RewardPeriod.objects.all().latest().pk, "New RewardPeriod does not match!"
    return new



