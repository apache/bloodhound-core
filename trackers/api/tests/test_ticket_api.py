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

from ...models import (
    Component,
    Milestone,
    Product,
    Ticket,
    Version,
)


class TicketApiTest(APITestCase):
    """Tests for ticket API"""

    def setUp(self):
        self.product = Product.objects.create(prefix="BH", name="Bloodhound")
        self.record1 = Ticket.objects.create(product=self.product, summary="BH #1")
        self.record2 = Ticket.objects.create(product=self.product, summary="BH #2")

        self.request_data = {
            "summary": "Example Summary",
        }

        self.bad_request_data = {
            "summary": "",
        }

    def test_get_all_tickets(self):
        response = self.client.get(
            reverse("product-tickets-list", kwargs={"product_prefix": "BH"})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            Ticket.objects.count(),
        )

    def test_get_ticket(self):
        response = self.client.get(
            reverse(
                "product-tickets-detail",
                kwargs={
                    "product_prefix": self.record1.product.prefix,
                    "product_ticket_id": self.record1.product_ticket_id,
                },
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['summary'], self.record1.summary)

    def test_get_invalid_ticket(self):
        response = self.client.get(
            reverse(
                "product-tickets-detail",
                kwargs={
                    "product_prefix": "BH",
                    "product_ticket_id": 9999,
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_ticket(self):
        response = self.client.post(
            reverse("product-tickets-list", kwargs={"product_prefix": "BH"}),
            self.request_data,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        record = Ticket.objects.get(
            product=self.product,
            product_ticket_id=response.data['product_ticket_id']
        )

        self.assertEqual(response.data['summary'], record.summary)

    def test_create_invalid_product(self):
        response = self.client.post(
            reverse(
                'product-tickets-list',
                kwargs={"product_prefix": "INVALID"}
            ),
            self.request_data,
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_missing_summary(self):
        response = self.client.post(
            reverse('product-tickets-list', kwargs={"product_prefix": "BH"}),
            self.bad_request_data,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_ticket(self):
        response = self.client.put(
            reverse(
                "product-tickets-detail",
                kwargs={
                    "product_prefix": self.record1.product.prefix,
                    "product_ticket_id": self.record1.product_ticket_id,
                },
            ),
            {"summary": "new summary"},
        )

        old_summary = self.record1.summary

        record = Ticket.objects.get(
            product=self.product,
            product_ticket_id=response.data['product_ticket_id']
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['summary'], record.summary)
        self.assertNotEqual(old_summary, record.summary)

    def test_update_ticket_bad_data(self):
        response = self.client.put(
            reverse(
                "product-tickets-detail",
                kwargs={
                    "product_prefix": self.record1.product.prefix,
                    "product_ticket_id": self.record1.product_ticket_id,
                },
            ),
            {"summary": ""},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_ticket(self):
        response = self.client.delete(
            reverse(
                'product-tickets-detail',
                kwargs={
                    "product_prefix": self.record1.product.prefix,
                    "product_ticket_id": self.record1.product_ticket_id,
                }
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Ticket.DoesNotExist):
            Ticket.objects.get(
                product=self.record1.product.prefix,
                product_ticket_id=self.record1.product_ticket_id,
            )


class ComponentApiTest(APITestCase):
    """Tests for component API"""

    def setUp(self):
        self.product = Product.objects.create(prefix="BH", name="Bloodhound")
        self.record1 = Component.objects.create(product=self.product, name="Component 1")
        self.record2 = Component.objects.create(product=self.product, name="Component 2")

        self.request_data = {
            "name": "Example Name",
        }

        self.bad_request_data = {
            "summary": "",
        }

    def test_get_all_components(self):
        response = self.client.get(
            reverse("product-components-list", kwargs={"product_prefix": "BH"})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            Component.objects.count(),
        )

    def test_get_component(self):
        response = self.client.get(
            reverse(
                "product-components-detail",
                kwargs={
                    "product_prefix": self.record1.product.prefix,
                    "name": self.record1.name,
                },
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.record1.name)

    def test_get_missing_component(self):
        response = self.client.get(
            reverse(
                "product-components-detail",
                kwargs={
                    "product_prefix": "BH",
                    "name": "not here",
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_component(self):
        response = self.client.post(
            reverse(
                "product-components-list",
                kwargs={"product_prefix": "BH"}
            ),
            self.request_data,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        record = Component.objects.get(
            product=self.product,
            name=response.data['name']
        )

        self.assertEqual(response.data['name'], record.name)

    def test_create_component_with_invalid_product(self):
        response = self.client.post(
            reverse(
                'product-components-list',
                kwargs={"product_prefix": "INVALID"}
            ),
            self.request_data,
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_component(self):
        new_name = "new name"
        response = self.client.put(
            reverse(
                "product-components-detail",
                kwargs={
                    "product_prefix": self.record1.product.prefix,
                    "name": self.record1.name,
                },
            ),
            {"name": new_name},
        )

        record = Component.objects.get(
            product=self.product,
            name=new_name,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(new_name, self.record1.name)
        self.assertEqual(record.name, new_name)

    def test_update_component_bad_data(self):
        response = self.client.put(
            reverse(
                "product-components-detail",
                kwargs={
                    "product_prefix": self.record1.product.prefix,
                    "name": self.record1.name,
                },
            ),
            {"summary": ""},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_component(self):
        response = self.client.delete(
            reverse(
                'product-components-detail',
                kwargs={
                    "product_prefix": self.record1.product.prefix,
                    "name": self.record1.name,
                }
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Component.DoesNotExist):
            Component.objects.get(
                product=self.record1.product.prefix,
                name=self.record1.name,
            )


class MilestoneApiTest(APITestCase):
    """Tests for milestone API"""

    def setUp(self):
        self.product = Product.objects.create(prefix="BH", name="Bloodhound")
        self.record1 = Milestone.objects.create(product=self.product, name="Milestone 1")
        self.record2 = Milestone.objects.create(product=self.product, name="Milestone 2")

        self.request_data = {
            "name": "Example Name",
            "description": "Example Description",
        }

        self.bad_request_data = {
            "summary": "",
        }

    def test_get_all_milestones(self):
        response = self.client.get(
            reverse("product-milestones-list", kwargs={"product_prefix": "BH"})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            Milestone.objects.count(),
        )

    def test_get_milestone(self):
        response = self.client.get(
            reverse(
                "product-milestones-detail",
                kwargs={
                    "product_prefix": self.record1.product.prefix,
                    "name": self.record1.name,
                },
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.record1.name)

    def test_get_missing_milestone(self):
        response = self.client.get(
            reverse(
                "product-milestones-detail",
                kwargs={
                    "product_prefix": "BH",
                    "name": "not here",
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_milestone(self):
        response = self.client.post(
            reverse(
                "product-milestones-list",
                kwargs={"product_prefix": "BH"}
            ),
            self.request_data,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        record = Milestone.objects.get(
            product=self.product,
            name=response.data['name']
        )

        self.assertEqual(response.data['description'], record.description)

    def test_create_milestone_with_invalid_product(self):
        response = self.client.post(
            reverse(
                'product-milestones-list',
                kwargs={"product_prefix": "INVALID"}
            ),
            self.request_data,
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_component(self):
        response = self.client.put(
            reverse(
                "product-milestones-detail",
                kwargs={
                    "product_prefix": self.record1.product.prefix,
                    "name": self.record1.name,
                },
            ),
            {"name": "new name"},
        )

        old_name = self.record1.name

        record = Milestone.objects.get(
            product=self.product,
            name=response.data['name']
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], record.description)
        self.assertNotEqual(old_name, record.name)

    def test_update_milestone_bad_data(self):
        response = self.client.put(
            reverse(
                "product-milestones-detail",
                kwargs={
                    "product_prefix": self.record1.product.prefix,
                    "name": self.record1.name,
                },
            ),
            {"summary": ""},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_milestone(self):
        response = self.client.delete(
            reverse(
                'product-milestones-detail',
                kwargs={
                    "product_prefix": self.record1.product.prefix,
                    "name": self.record1.name,
                }
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Milestone.DoesNotExist):
            Milestone.objects.get(
                product=self.record1.product.prefix,
                name=self.record1.name,
            )


class VersionApiTest(APITestCase):
    """Tests for component API"""

    def setUp(self):
        self.product = Product.objects.create(prefix="BH", name="Bloodhound")
        self.record1 = Version.objects.create(product=self.product, name="Version 1")
        self.record2 = Version.objects.create(product=self.product, name="Version 2")

        self.request_data = {
            "name": "Example Name",
            "description": "Example description",
        }

        self.bad_request_data = {
            "summary": "",
        }

    def test_get_all_versions(self):
        response = self.client.get(
            reverse("product-versions-list", kwargs={"product_prefix": "BH"})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            Version.objects.count(),
        )

    def test_get_version(self):
        response = self.client.get(
            reverse(
                "product-versions-detail",
                kwargs={
                    "product_prefix": self.record1.product.prefix,
                    "name": self.record1.name,
                },
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.record1.name)

    def test_get_missing_version(self):
        response = self.client.get(
            reverse(
                "product-versions-detail",
                kwargs={
                    "product_prefix": "BH",
                    "name": "not here",
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_version(self):
        response = self.client.post(
            reverse(
                "product-versions-list",
                kwargs={"product_prefix": "BH"}
            ),
            self.request_data,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        record = Version.objects.get(
            product=self.product,
            name=response.data['name']
        )

        self.assertEqual(response.data['description'], record.description)

    def test_create_version_with_invalid_product(self):
        response = self.client.post(
            reverse(
                'product-versions-list',
                kwargs={"product_prefix": "INVALID"}
            ),
            self.request_data,
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_version(self):
        new_name = "new name"
        response = self.client.put(
            reverse(
                "product-versions-detail",
                kwargs={
                    "product_prefix": self.record1.product.prefix,
                    "name": self.record1.name,
                },
            ),
            {"name": new_name},
        )

        old_name = self.record1.name

        record = Version.objects.get(
            product=self.product,
            name=response.data['name']
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(new_name, old_name)
        self.assertEqual(record.name, new_name)

    def test_update_version_bad_data(self):
        response = self.client.put(
            reverse(
                "product-versions-detail",
                kwargs={
                    "product_prefix": self.record1.product.prefix,
                    "name": self.record1.name,
                },
            ),
            {"summary": ""},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_version(self):
        response = self.client.delete(
            reverse(
                'product-versions-detail',
                kwargs={
                    "product_prefix": self.record1.product.prefix,
                    "name": self.record1.name,
                }
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Version.DoesNotExist):
            Version.objects.get(
                product=self.record1.product.prefix,
                name=self.record1.name,
            )
