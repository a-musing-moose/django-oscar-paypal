import urlparse

from django.db import models
from django.utils.translation import ugettext_lazy as _


class PaymentNotification(models.Model):
    
    raw_request = models.TextField(max_length=512)
    txn_type = models.CharField(_('Transaction type'), max_length=128)
    txn_id = models.CharField(
        _('Transaction Id'),
        max_length=128,
        blank=True,
        null=True
    ) # For subscriptions based notifications this is blank
    date_created = models.DateTimeField(auto_now_add=True)

    def value(self, key):
        ctx = self.context
        if key in ctx:
            return ctx[key][0].decode('utf8')
        return None
        
    @property
    def context(self):
        return urlparse.parse_qs(self.raw_response)

    def __unicode__(self):
        return u'%d: %s' % (self.id, self.txn_type)

    class Meta:
        ordering = ('-date_created',)
        app_label = 'paypal'
