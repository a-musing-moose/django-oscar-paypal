import requests

from django.views.generic import View
from django.conf import settings
from django.http import HttpResponse
from django.db import transaction

from paypal.ipn.models import PaymentNotification
from paypal.ipn.signals import ipn_received


class IPNHandlerView(View):

	http_method_names = [u'post', u'options']

	def post(self, request, *args, **kwargs):
		txn_id = self.request.POST.get('txn_id')
		if not txn_id:
			return HttpResponse("Invalid parameters")

		if self.already_exists():
			return HttpResponse("Success")

		if self.is_verified():
			ipn = self.create_ipn()
			ipn_received.send(sender=self, instance=ipn)
			return HttpResponse("Success")

		return HttpResponse("Unable to Verify")

	@transaction.commit_on_success
	def create_ipn(self):
		return PaymentNotification.object.create(
			raw_request=self.request.raw_post_data,
			txn_id=self.request.POST.get('txn_id'),
			txn_type=self.request.POST.get('txn_type')
		)

	def already_exists(self):
		txn_id = self.request.POST.get('txn_id')
		try:
			PaymentNotification.objects.get(txn_id=txn_id)
		except PaymentNotification.DoesNotExist:
			return False
		return True

	def is_verified(self):
		raw_request = self.request.raw_post_data
		verify_data = "cmd=_notify-validate&%s" % raw_request

		url = 'https://www.paypal.com/cgi-bin/webscr'
		if getattr(settings, 'PAYPAL_SANDBOX_MODE', True):
			url = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
		try:
			response = requests.post(url, data=verify_data, timeout=3)
		except requests.exceptions.Timeout:
			return False
		else:
			return "VERIFIED" in response