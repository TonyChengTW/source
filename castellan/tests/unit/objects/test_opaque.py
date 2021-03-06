# Copyright (c) 2015 The Johns Hopkins University/Applied Physics Laboratory
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Test cases for the opaque data class.
"""

from castellan.common.objects import opaque_data
from castellan.tests import base


class OpaqueDataTestCase(base.TestCase):

    def _create_data(self):
        return opaque_data.OpaqueData(self.data, self.name)

    def setUp(self):
        self.data = bytes(b"secret opaque data")
        self.name = 'my opaque'
        self.opaque_data = self._create_data()

        super(OpaqueDataTestCase, self).setUp()

    def test_get_format(self):
        self.assertEqual('Opaque', self.opaque_data.format)

    def test_get_encoded(self):
        self.assertEqual(self.data, self.opaque_data.get_encoded())

    def test_get_name(self):
        self.assertEqual(self.name, self.opaque_data.name)

    def test___eq__(self):
        self.assertTrue(self.opaque_data == self.opaque_data)
        self.assertTrue(self.opaque_data is self.opaque_data)

        self.assertFalse(self.opaque_data is None)
        self.assertFalse(None == self.opaque_data)

        other_opaque_data = opaque_data.OpaqueData(self.data, self.name)
        self.assertTrue(self.opaque_data == other_opaque_data)
        self.assertFalse(self.opaque_data is other_opaque_data)

    def test___ne___none(self):
        self.assertTrue(self.opaque_data is not None)
        self.assertTrue(None != self.opaque_data)

    def test___ne___data(self):
        other_opaque = opaque_data.OpaqueData(b'other data', self.name)
        self.assertTrue(self.opaque_data != other_opaque)

    def test___ne___name(self):
        other_opaque = opaque_data.OpaqueData(self.data, "other opaque")
        self.assertTrue(self.opaque_data != other_opaque)
