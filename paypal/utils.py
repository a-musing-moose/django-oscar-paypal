from django.conf import settings


def get_recurring_predicate():
    if hasattr(settings, "PAYPAL_RECURRING_PREDICATE"):
        seg = getattr(settings, "PAYPAL_RECURRING_PREDICATE").split('.')
        module = __import__('.'.join(seg[:-1]))
        for component in seg[1:-1]:
            module = getattr(module, component)
        return getattr(module, seg[-1])
    else:
        return lambda product: None


get_recurring_profile = get_recurring_predicate()
