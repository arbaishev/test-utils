# coding=utf-8
# future
from __future__ import absolute_import, unicode_literals

from enum import Enum

from django.shortcuts import render
from errand_boy.transports.unixsocket import UNIXSocketTransport
from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from rest_framework.views import APIView
from pytils.translit import slugify, detranslify, translify
from pytils.numeral import get_plural
from .forms import TestForm


class PaymentMethod(Enum):
    CASH = 0
    CASHLESS = 1

    @classmethod
    def model_choices(cls):
        return (cls.CASH.value, "Наличные"), (cls.CASHLESS.value, "Безналичные")


class CheckType(Enum):
    SELL = 0
    SELL_RETURN = 1

    @classmethod
    def model_choices(cls):
        return (cls.SELL.value, "Приход"), (cls.SELL_RETURN.value, "Возврат прихода")


class RequestSchema(Schema):
    payment_method = EnumField(PaymentMethod, required=True, load_from="paymentMethod")
    type = EnumField(CheckType, required=True)
    int_for_plural = fields.Int(required=True)
    text_for_translite = fields.Str(required=True)
    text_for_slug = fields.Str(required=True)


class TestView(APIView):
    def post(self, request):
        data, errors = RequestSchema().load(request.data)

        errand_boy_transport = UNIXSocketTransport()
        out, err, returncode = errand_boy_transport.run_cmd("wkhtmltopdf -V")

        translified_text = translify(data["text_for_translite"])

        result = {
            "type": str(data["type"]),
            "type_value": str(data["type"].value),
            "payment_method": str(data["payment_method"]),
            "payment_method_value": str(data["payment_method"].value),
            "wkhtml": out,
            "slug": slugify(data["text_for_slug"]),
            "translite": translified_text,
            "detranslite": detranslify(translified_text),
            "plural_first": get_plural(data["int_for_plural"], ("клиенту", "клиентам", "клиентам")),
            "plural_second": get_plural(data["int_for_plural"], "секунду,секунды,секунд"),
        }

        return render(request, "test.html", result)

    def get(self, request):
        testform = TestForm()
        return render(request, "test_form.html", {"form": testform})

