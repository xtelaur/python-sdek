# coding: utf-8

from __future__ import unicode_literals, print_function

import datetime
import unittest

import mock

from cdek import api, exceptions


@mock.patch('cdek.api.urlopen')
class CdekApiTest(unittest.TestCase):

    def setUp(self):
        self.reg_user = api.CdekCalc('123456', '123456')
        self.unreg_user = api.CdekCalc()

    def test_valid_get_secure(self, urlopen):
        self.assertEqual(self.reg_user._get_secure(
            datetime.datetime.today().date(), self.reg_user.auth_password),
            'c5750d7c97a89aa33b8e030d4c7a4847')

        self.assertNotEqual(self.reg_user._get_secure(
            datetime.datetime.today().date() - datetime.timedelta(days=2),
            self.reg_user.auth_password), 'c5750d7c97a89aa33b8e030d4c7a4847')