from rest_framework.decorators import api_view
from rest_framework.response import Response

from lib.brains.client import get_client
from lib.brains.errors import BraintreeResultError
from lib.brains.forms import SubscriptionForm
from lib.brains.models import BraintreeSubscription
from lib.brains.serializers import (
    LocalSubscription, Namespaced, Subscription)
from solitude.base import NonDeleteModelViewSet
from solitude.errors import FormError
from solitude.logger import getLogger

log = getLogger('s.brains')


@api_view(['POST'])
def create(request):
    client = get_client().Subscription
    form = SubscriptionForm(request.DATA)

    if not form.is_valid():
        raise FormError(form.errors)

    data = form.braintree_data
    result = client.create(data)

    if not result.is_success:
        log.warning('Error on creating subscription: {0}'
                    .format(result.message))
        raise BraintreeResultError(result)

    braintree_subscription = result.subscription
    log.info('Subscription created in braintree: {0}'
             .format(braintree_subscription.id))

    subscription = BraintreeSubscription.objects.create(
        paymethod=form.cleaned_data['paymethod'],
        seller_product=form.seller_product,
        provider_id=braintree_subscription.id
    )
    log.info('Subscription created in solitude: {0}'.format(subscription.pk))

    res = Namespaced(
        LocalSubscription(instance=subscription),
        Subscription(instance=braintree_subscription)
    )
    return Response(res.data, status=201)


class SubscriptionViewSet(NonDeleteModelViewSet):
    queryset = BraintreeSubscription.objects.all()
    serializer_class = LocalSubscription
    filter_fields = ('paymethod', 'paymethod__braintree_buyer',
                     'paymethod__braintree_buyer__buyer',
                     'seller_product')

    def create(self, *args, **kw):
        # Subscriptions should be created using the braintree
        # API so that they can be correctly set up.
        return Response(status=405)
