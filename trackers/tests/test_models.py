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
from ..models import Product, Ticket


class ProductTest(TestCase):
    """Tests for Product model"""
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


class TicketTest(TestCase):
    """Test for Ticket model"""
    def setUp(self):
        self.product = Product.objects.create(
            prefix='BH',
            name='Bloodhound',
            description='Apache Bloodhound',
        )

    def test_ticket_create_sets_product_ticket_number(self):
        ticket = Ticket.objects.create(
            product=self.product,
        )
        self.assertIsNotNone(ticket.product_ticket_id)

    def test_ticket_create_sets_unique_product_ticket_number(self):
        ticket1 = Ticket.objects.create(
            product=self.product,
        )
        ticket2 = Ticket.objects.create(
            product=self.product,
        )
        self.assertNotEqual(ticket1.product_ticket_id, ticket2.product_ticket_id)

    def test_ticket_create_uses_unique_product_ticket_number_when_tickets_deleted(self):
        ticket1 = Ticket.objects.create(
            product=self.product,
        )
        ticket2 = Ticket.objects.create(
            product=self.product,
        )
        ticket1.delete()
        ticket3 = Ticket.objects.create(
            product=self.product,
        )
        self.assertIsNotNone(ticket1.product_ticket_id)
        self.assertIsNotNone(ticket2.product_ticket_id)
        self.assertIsNotNone(ticket3.product_ticket_id)
        self.assertNotEqual(ticket2.product_ticket_id, ticket3.product_ticket_id)
