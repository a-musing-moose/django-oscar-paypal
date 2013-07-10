from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt

from paypal.ipn.views import IPNHandlerView


urlpatterns = patterns('',
    # View for handling IPN requests
    url(
        r'^receiver/',
        csrf_exempt(IPNHandlerView.as_view()),
        name='paypal-ipn-receiver'
    ),
)
