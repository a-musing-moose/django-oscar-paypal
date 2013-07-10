from django.contrib import admin
from paypal import models


admin.site.register(models.PaymentNotification)
