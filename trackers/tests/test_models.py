#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

from django.test import TestCase
from ..models import Product


class ProductTest(TestCase):
    """Test modules for Product model"""
    def setUp(self):
        Product.objects.create(
            prefix='BHD',
            name='Bloodhound Legacy',
            description='The original Apache Bloodhound',
        )
        Product.objects.create(
            prefix='BH',
            name='Bloodhound',
            description='The future of Apache Bloodhound',
        )

    def test_product_name(self):
        bhd = Product.objects.get(prefix='BHD')
        bh = Product.objects.get(prefix='BH')

        self.assertEqual(bhd.name, "Bloodhound Legacy")
        self.assertEqual(bh.name, "Bloodhound")
