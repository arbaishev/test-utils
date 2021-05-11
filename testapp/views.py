# coding=utf-8
# future
from __future__ import absolute_import, unicode_literals

from enum import Enum

from django.shortcuts import render
from errand_boy.transports.unixsocket import UNIXSocketTransport
from marshmallow import Schema
from marshmallow_enum import EnumField
from rest_framework.views import APIView


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


class TestView(APIView):
    def post(self, request):
        data, errors = RequestSchema().load(request.data)

        errand_boy_transport = UNIXSocketTransport()
        out, err, returncode = errand_boy_transport.run_cmd("wkhtmltopdf -V")
        result = {
            "type": str(data["type"]),
            "type_value": str(data["type"].value),
            "payment_method": str(data["payment_method"]),
            "payment_method_value": str(data["payment_method"].value),
            "wkhtml": out,
        }
        return render(request, "test.html", result)
