from rest_framework.decorators import api_view
from rest_framework.response import Response

from lib.brains import serializers
from lib.brains.client import get_client
from lib.brains.errors import BraintreeResultError
from lib.brains.forms import PaymentMethodForm
from lib.brains.models import BraintreePaymentMethod
from solitude.base import NonDeleteModelViewSet
from solitude.constants import PAYMENT_METHOD_CARD
from solitude.errors import FormError
from solitude.logger import getLogger

log = getLogger('s.brains')


@api_view(['POST'])
def create(request):
    client = get_client().PaymentMethod
    form = PaymentMethodForm(request.DATA)

    if not form.is_valid():
        raise FormError(form.errors)

    buyer = form.buyer
    braintree_buyer = form.braintree_buyer
    result = client.create(form.braintree_data)

    if not result.is_success:
        log.warning('Error on creating Payment method: {0}, {1}'
                    .format(buyer.uuid, result.message))
        raise BraintreeResultError(result)

    braintree_method = result.payment_method
    log.info('PaymentMethod created for: {0}'.format(buyer.uuid))

    solitude_method = BraintreePaymentMethod.objects.create(
        braintree_buyer=braintree_buyer,
        type=PAYMENT_METHOD_CARD,
        type_name=braintree_method.card_type,
        provider_id=braintree_method.token,
        truncated_id=result.payment_method.last_4
    )
    log.info('Method {0} created.'.format(solitude_method.pk))

    res = serializers.Namespaced(
        serializers.LocalPayMethod(instance=solitude_method),
        serializers.PayMethod(instance=braintree_method)
    )
    return Response(res.data, status=201)


class PaymentMethodViewSet(NonDeleteModelViewSet):
    queryset = BraintreePaymentMethod.objects.filter()
    serializer_class = serializers.LocalPayMethod
    filter_fields = ('braintree_buyer', 'braintree_buyer__buyer__uuid',
                     'active')

    def create(self, *args, **kw):
        # You must create a payment method through the braintree payment method
        # API to ensure that the objects are in sync.
        return Response('Call braintree payment method create', status=405)
