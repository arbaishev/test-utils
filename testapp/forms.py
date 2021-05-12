# coding=utf-8
# future
from __future__ import absolute_import, unicode_literals

from django import forms


class TestForm(forms.Form):
    type = forms.ChoiceField((("SELL", "SELL"), ("SELL_RETURN", "SELL_RETURN"),))
    payment_method = forms.ChoiceField((("CASH", "CASH"), ("CASHLESS", "CASHLESS"),))
    int_for_plural = forms.IntegerField()
    text_for_translite = forms.CharField()
    text_for_slug = forms.CharField()
