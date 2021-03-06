from datetime import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

from aesfield.field import AESField

from .field import HashField
from solitude.base import Model


class Buyer(Model):
    uuid = models.CharField(max_length=255, db_index=True, unique=True)
    pin = HashField(blank=True, null=True)
    pin_confirmed = models.BooleanField(default=False)
    pin_failures = models.IntegerField(default=0)
    pin_locked_out = models.DateTimeField(blank=True, null=True)
    pin_was_locked_out = models.BooleanField(default=False)
    active = models.BooleanField(default=True, db_index=True)
    new_pin = HashField(blank=True, null=True)
    needs_pin_reset = models.BooleanField(default=False)
    email = AESField(blank=True, null=True, aes_key='buyeremail:key')

    class Meta(Model.Meta):
        db_table = 'buyer'

    @property
    def locked_out(self):
        if not self.pin_locked_out:
            return False

        if ((datetime.now() - self.pin_locked_out).seconds >
                settings.PIN_FAILURE_LENGTH):
            self.clear_lockout()
            return False

        return True

    def clear_lockout(self, clear_was_locked=False):
        self.pin_failures = 0
        self.pin_locked_out = None
        if clear_was_locked:
            self.pin_was_locked_out = False
        self.save()

    def incr_lockout(self):
        # Use F to avoid race conditions, although this means an extra
        # query to check if we've gone over the limit.
        self.pin_failures = models.F('pin_failures') + 1
        self.save()

        failing = self.reget()
        if failing.pin_failures >= settings.PIN_FAILURES:
            failing.pin_locked_out = datetime.now()
            failing.pin_was_locked_out = True
            failing.save()
            # Indicate to the caller that we are now locked out.
            return True

        return False

    def get_uri(self):
        return reverse('generic:buyer-detail', kwargs={'pk': self.pk})
