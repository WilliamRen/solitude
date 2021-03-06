.. _braintree:

Braintree
#########

Make sure your :ref:`braintree-settings` are up to date so that
Solitude can connect to the API.

Tokens
------

Calls braintree `ClientToken.generate <https://developers.braintreepayments.com/javascript+python/reference/request/client-token/generate>`_:

.. http:post:: /braintree/token/generate/

    :>json string token: the token returned by Braintree.
    :status 200: token successfully generated.

Customers
---------

Creates a customer in Braintree and the corresponding buyer and Braintree buyer
in solitude. If the buyer exists in solitude already, it is not created. If the
customer exists in Braintree already, it is not created.

.. http:post:: /braintree/customer/

    :<json string uuid: the uuid of the buyer in solitude.

    .. code-block:: json

        {
            "braintree": {
                "created_at": "2015-05-06T15:35:41.519",
                "id": "customer-id",
                "updated_at": "2015-05-06T15:35:41.519"
            },
            "mozilla": {
                "active": true,
                "braintree_id": "customer-id",
                "buyer": "/generic/buyer/3/",
                "counter": 0,
                "created": "2015-05-06T15:35:41.523",
                "id": 2,
                "modified": "2015-05-06T15:35:41.523",
                "resource_pk": 2,
                "resource_uri": "/braintree/mozilla/buyer/2/"
            }
        }

    :>json string braintree id: id.
    :>json string braintree created_at: created date and time.
    :>json string braintree updated_at: updated date and time.

    :status 201: customer and Braintree buyer successfully created.

.. _braintree-buyer-label:

Data stored in solitude
+++++++++++++++++++++++

Some information is stored in solitude after creating a customer.

.. http:get:: /braintree/mozilla/buyer/<buyer id>/

    :<json string uuid: the uuid of the buyer in solitude.
    :<json string nonce: the payment nonce returned by Braintree.

    .. code-block:: json

        {
            "active": true,
            "braintree_id": "customer-id",
            "buyer": "/generic/buyer/3/",
            "counter": 0,
            "created": "2015-05-06T15:35:41.523",
            "id": 2,
            "modified": "2015-05-06T15:35:41.523",
            "resource_pk": 2,
            "resource_uri": "/braintree/mozilla/buyer/2/"
        }

    :>json boolean active: if the buyer is currently active.
    :>json string braintree_id: the id of the customer on Braintree. This field
                                is read only.
    :>json string buyer: URI to :ref:`a buyer object <buyer-label>`

.. http:patch:: /braintree/mozilla/buyer/<buyer id>/

    :<json boolean active: if the buyer is currently active.

.. http:get:: /braintree/mozilla/buyer/

    :query buyer: the primary key of the buyer.
    :query active: the active status.

.. _payment-methods-label:

Payment Methods
---------------

Creates a payment method in Braintree and the corresponding payment method in
solitude.

.. http:post:: /braintree/paymethod/

    :<json string uuid: the uuid of the buyer in solitude.
    :<json string nonce: the payment nonce returned by Braintree.

    .. code-block:: json

        {
            "braintree": {
                "created_at": "2015-05-05T14:22:26.650",
                "token": "da-token",
                "updated_at": "2015-05-05T14:22:26.650"
            },
            "mozilla": {
                "active": true,
                "braintree_buyer": "/braintree/mozilla/buyer/16/",
                "counter": 0,
                "created": "2015-05-05T14:22:26.656",
                "id": 4,
                "modified": "2015-05-05T14:22:26.656",
                "provider_id": "da-token",
                "resource_pk": 4,
                "resource_uri": "/braintree/mozilla/paymethod/4/",
                "truncated_id": "7890",
                "type": 1,
                "type_name": "visa"
            }
        }

    :>json string braintree token: id of the payment method in braintree.
    :>json string braintree created_at: created date and time.
    :>json string braintree updated_at: updated date and time.

    :status 201: payment method created.

Data stored in solitude
+++++++++++++++++++++++

Some information about the payment method is stored in solitude.

.. http:get:: /braintree/mozilla/paymethod/<method id>/

    .. code-block:: json

        {
          "active": true,
          "braintree_buyer": "/braintree/mozilla/buyer/2/",
          "counter": 0,
          "created": "2015-05-05T14:25:38",
          "id": 1,
          "modified": "2015-05-05T14:25:38",
          "provider_id": "da-token",
          "resource_pk": 1,
          "resource_uri": "/braintree/mozilla/paymethod/1/",
          "truncated_id": "some",
          "type": 1,
          "type_name": "visa"
        }

    :>json boolean active: active flag for the method.
    :>json string braintree_buyer: URI to :ref:`a braintree buyer object <braintree-buyer-label>`.
    :>json string provider_id: an id for the payment method on the provider, this field is read only.
    :>json string truncated_id: a truncated id of the payment type, for example
                                for a credit card, the last 4 digits, this field is read only.
    :>json int type: `1` for credit card is currently the only one supported, this field is read only.
    :>json string type_name: name of the type of purchase, this field is read only.

.. http:patch:: /braintree/mozilla/paymethod/<method id>/

    :<json boolean active: if the payment method is currently active.

.. http:get:: /braintree/mozilla/paymethod/

    :query braintree_buyer: the primary key of the braintree_buyer.
    :query braintree_buyer__buyer__uuid: the uuid for the buyer.
    :query active: the active status.

.. _subscription-label:

Subscriptions
-------------

Create a subscription in Braintree and the corresponding subscription in
solitude.

.. http:post:: /braintree/subscription/

    :<json string paymethod: the uri of the payment method.
    :<json string plan: the id of the plan being purchased.

    .. code-block:: json

        {
            "braintree": {
                "created_at": "2015-05-06T13:34:53.746",
                "id": "some:id",
                "updated_at": "2015-05-06T13:34:53.746"
            },
            "mozilla": {
                "active": true,
                "counter": 0,
                "created": "2015-05-06T13:34:53.763",
                "id": 1,
                "modified": "2015-05-06T13:34:53.763",
                "paymethod": "/braintree/mozilla/paymethod/1/",
                "provider_id": "some:id",
                "resource_pk": 1,
                "resource_uri": "/braintree/mozilla/subscription/1/",
                "seller_product": "/generic/product/1/"
            }
        }

    :>json string braintree id: id of the subscription in braintree.
    :>json string braintree created_at: created date and time.
    :>json string braintree updated_at: updated date and time.

    :status 201: payment method created.


Data stored in solitude
+++++++++++++++++++++++

Some information about the subscripton is stored in solitude.

.. http:get:: /braintree/mozilla/subscription/<subscription id>/

    .. code-block:: json

        {
            "active": true,
            "counter": 0,
            "created": "2015-05-01T18:21:49",
            "id": 1,
            "paymethod": "/braintree/mozilla/paymethod/2/",
            "modified": "2015-05-01T18:21:49",
            "provider_id": "some:id",
            "resource_pk": 1,
            "resource_uri": "/braintree/mozilla/subscription/1/",
            "seller_product": "/generic/product/2/"
        }

    :>json boolean active: active flag for the method.
    :>json string provider_id: an id for the subscription on the provider,
                               this field is read only.
    :>json string paymethod: the URI to `a payment object <payment-methods-label>`_.
    :>json string seller_product: the URI to `a seller product
                                  <seller-product>`_.

.. http:patch:: /braintree/mozilla/subscription/<subscription id>/

    :<json boolean active: if the subscription is currently active.

.. http:get:: /braintree/mozilla/subscription/

    :query paymethod: the primary key of the payment method.
    :query paymethod__braintree_buyer: the primary key of the braintree buyer.
    :query paymethod__braintree_buyer__buyer: the primary key of the buyer.
    :query seller_product: the primary key of the product.

Webhook
-------

When Braintree completes certain actions, they will make a request to the
configured webhook URL. That will be `<payments-service https://github.com/mozilla/payments-service/>`_
which then passes it on to this endpoint. For more information see the
`Braintree documentation <https://developers.braintreepayments.com/javascript+python/reference/general/webhooks>`_.

.. http:get:: /braintree/webhook/

    :query bt_challenge string: the bt_challenge issued by Braintree.
    :>json string: a token returned by the Braintree verify API.

    :status 200: token verified and returned.

.. http:post:: /braintree/webhook/

    :<json bt_signature: the bt_signature issued by Braintree.
    :<json bt_payload: the bt_payload issued by Braintree.

    :status 204: webhook parsed successfully.
