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
from hypothesis import example, given, strategies as st
from hypothesis.extra.django import TestCase
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status

from ...models import Product

name_st = st.text(
    st.characters(
        blacklist_characters="/",
        max_codepoint=1000,
        blacklist_categories=("Cc", "Cs")
    ),
    min_size=1
).map(lambda x: x.strip()).filter(lambda s: len(s) > 0)


class CommonAPIPropertiesTestCase(TestCase):
    """Common tests for API"""

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.product = Product.objects.create(prefix="BH", name="Bloodhound")
        self.list_uri = reverse(
            self.list_view_name,
            kwargs={"product_prefix": "BH"}
        )


class NameTestsMixin:
    @given(name=name_st)
    @example("next 1.x")
    def test_create(self, name):
        data = {
            "name": name,
            "description": "Example Description",
        }

        response = self.client.post(self.list_uri, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ComponentAPIPropertiesTest(CommonAPIPropertiesTestCase, NameTestsMixin):
    """Hypothesis tests for component API"""

    def setUp(self):
        self.list_view_name = "product-components-list"
        super().setUp()


class MilestoneAPIPropertiesTest(CommonAPIPropertiesTestCase, NameTestsMixin):
    """Hypothesis tests for milestone API"""

    def setUp(self):
        self.list_view_name = "product-milestones-list"
        super().setUp()


class VersionAPIPropertiesTest(CommonAPIPropertiesTestCase, NameTestsMixin):
    """Hypothesis tests for version API"""

    def setUp(self):
        self.list_view_name = "product-versions-list"
        super().setUp()
