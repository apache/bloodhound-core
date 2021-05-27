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

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from ...models import Product


class ProductsApiTest(APITestCase):
    """Test for GET all products API"""

    def setUp(self):
        self.ally = Product.objects.create(prefix='ALY', name='Project Alice')
        self.bob = Product.objects.create(prefix='BOB', name='Project Robert')

        self.new_product_data = {
            'prefix': 'CAR',
            'name': 'Project Caroline',
        }

        self.product_data = {
            'prefix': self.ally.prefix,
            'name': 'Project Alan',
        }

        self.bad_product_data = {
            'prefix': self.bob.prefix,
            'name': '',
        }

    def test_get_all_products(self):
        response = self.client.get(reverse('product-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            Product.objects.count(),
        )

    def test_get_product(self):
        response = self.client.get(
            reverse('product-detail', args=[self.ally.prefix]),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['prefix'], self.ally.prefix)
        self.assertEqual(response.data['name'], self.ally.name)

    def test_get_invalid_product(self):
        response = self.client.get(
            reverse('product-detail', args=['randomnonsense'])
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_product(self):
        response = self.client.post(
            reverse('product-list'),
            self.new_product_data,
        )

        product = Product.objects.get(prefix=self.new_product_data['prefix'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(product.prefix, self.new_product_data['prefix'])
        self.assertEqual(product.name, self.new_product_data['name'])

    def test_create_bad_product(self):
        response = self.client.post(
            reverse('product-list'),
            self.bad_product_data,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product(self):
        response = self.client.put(
            reverse('product-detail', args=[self.ally.prefix]),
            self.product_data,
        )

        product = Product.objects.get(prefix=self.product_data['prefix'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.ally.name, product.name)
        self.assertEqual(self.product_data['prefix'], product.prefix)
        self.assertEqual(self.product_data['name'], product.name)

    def test_update_product_bad_data(self):
        response = self.client.put(
            reverse('product-detail', args=[self.bob.prefix]),
            self.bad_product_data,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_product(self):
        response = self.client.delete(
            reverse('product-detail', args=[self.ally.prefix]),
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
