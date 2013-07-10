import django.dispatch


ipn_received = django.dispatch.Signal(providing_args=["instance"])