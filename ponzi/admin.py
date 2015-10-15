from django.contrib import admin

from .models import AddressPair, RewardPeriod, Tx

# Register your models here.

class TxAdmin(admin.ModelAdmin):
#    readonly_fields=('txid','date','amount','confirmed','addresspair')
    list_display = ('txid','date','amount','rewardperiod','rewarded', 'confirmed', 'isreward')

admin.site.register(AddressPair)
admin.site.register(RewardPeriod)
admin.site.register(Tx, TxAdmin)
