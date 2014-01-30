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
            datetime.datetime.strptime('2013-05-30', '%Y-%m-%d'), self.reg_user.auth_password),
            '21de6125dbaac7adf68007c6bcf9ac98')

        self.assertNotEqual(self.reg_user._get_secure(
            datetime.datetime.today().date(), self.reg_user.auth_password),
            '21de6125dbaac7adf68007c6bcf9ac98')