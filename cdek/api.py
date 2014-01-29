# coding: utf-8

"""
cdek.api

This module implements the CDEK API for registered and unregistered clients.

To use in a python:

    from cdek.api import CdekCalc

    # for clients without API ID
    delivery = CdekCalc()
    delivery.calculate_price(sender_city_id="270", receiver_city_id="44", weight="0.1", volume="0.1", tariff_id="1")

    # for clients with API ID
    delivery = CdekCalc(auth_login="123456", auth_password="123456")
    delivery.calculate_price(sender_city_id="270", receiver_city_id="44", weight="0.1", volume="0.1")

"""

from __future__ import unicode_literals

import datetime
import json
from hashlib import md5

try:
    from urllib2 import urlopen, Request
    from urllib2 import urlopen
    from urllib import urlencode
except ImportError:
    from urllib.request import urlopen, Request
    import urllib.parse as urlparse
    from urllib.parse import urlencode

from .exceptions import CdekException
from .conf import API_HOST, API_PORT, API_CALC_PRICE


class CdekCalc(object):

    API_VERSION = "1.0"
    USER_ = 1  # registered user
    UNREG_USER = 2  # unregistered user

    def __init__(self, auth_login=None, auth_password=None):

        self.auth_login = auth_login
        self.auth_password = auth_password
        self.port = API_PORT

    def _is_registered_user(self):
        return self.auth_login and self.auth_password

    @staticmethod
    def _get_secure(date, auth_password):
        """(date, string) -> string

        Return secure key for API access

            secure = md5(dateExecute + "&" + authPassword)

            dateExecute - delivery date
            authPassword - client API password

        Details in CDEK API docs

        """
        secure_key = md5()
        secure_key.update("{0}&{1}".format(date, auth_password).encode("utf8"))
        return secure_key.hexdigest()

    def _get_url(self, target):
        """
        Return request API url
        """
        port = "" if self.port == 80 else ":%d" % self.port
        protocol = "http://"
        base_full_url = "%s%s/%s%s" % (protocol, API_HOST, target, port)
        return base_full_url

    def request(self, target, **params):
        """
        Return json from API response
        """

        if self._is_registered_user():
            # TODO Check date
            pass

        current_date = datetime.datetime.today().date()
        url = self._get_url(target)
        data = json.dumps({
            "version": self.API_VERSION,
            "dateExecute": current_date.strftime("%Y-%m-%d"),
            "secure": self._get_secure(current_date, self.auth_password),
            "authLogin": self.auth_login,
            "senderCityId": params["sender_city_id"],
            "receiverCityId": params["receiver_city_id"],
            "tariffId": params.get("tariff_id", 1),
            "goods": [{"weight": params["weight"], "volume": params["volume"]}]
        }).encode('utf-8')

        headers = {
            "User-Agent": "python/client",
            "Content-Type": "application/json",
            "Content-length": len(data)
        }

        # TODO: maybe just use 'requests' lib?
        request = Request(url)
        request.headers.update(headers)
        result = urlopen(request, data, 15)

        return result.read()

    def calculate_price(self, **params):
        price = self.request(API_CALC_PRICE, **params)
        return price