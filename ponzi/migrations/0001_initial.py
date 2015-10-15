# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddressPair',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_addr', models.CharField(unique=True, max_length=35)),
                ('site_addr', models.CharField(max_length=35, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RewardPeriod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'get_latest_by': 'date',
            },
        ),
        migrations.CreateModel(
            name='Tx',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('txid', models.CharField(max_length=64, null=True, blank=True)),
                ('isreward', models.BooleanField(default=False)),
                ('amount', models.DecimalField(max_digits=16, decimal_places=8)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('confirmed', models.BooleanField(default=False)),
                ('rewarded', models.BooleanField(default=False)),
                ('donation', models.BooleanField(default=False)),
                ('addresspair', models.ForeignKey(to='ponzi.AddressPair')),
                ('rewardperiod', models.ForeignKey(to='ponzi.RewardPeriod', null=True)),
                ('rewardtx', models.OneToOneField(null=True, blank=True, to='ponzi.Tx')),
            ],
        ),
    ]
