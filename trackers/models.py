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

import logging

from django.db import models

logger = logging.getLogger(__name__)


class Product(models.Model):
    prefix = models.TextField(primary_key=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    owner = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'bloodhound_product'


class ProductConfig(models.Model):
    """Possibly legacy table - keeping for now"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    section = models.TextField()
    option = models.TextField()
    value = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'bloodhound_productconfig'
        unique_together = (('product', 'section', 'option'),)


class ProductResourceMap(models.Model):
    """Possibly legacy model - keeping for now"""

    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    resource_type = models.TextField(blank=True, null=True)
    resource_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'bloodhound_productresourcemap'


class Component(models.Model):
    name = models.TextField(primary_key=True)
    owner = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    product = models.ForeignKey(
        Product,
        db_column="product",
        on_delete=models.PROTECT,
    )

    class Meta:
        db_table = 'component'
        unique_together = (('name', 'product'),)


class Enum(models.Model):
    type = models.TextField(primary_key=True)
    name = models.TextField()
    value = models.TextField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    class Meta:
        db_table = 'enum'
        unique_together = (('type', 'name', 'product'),)


class Milestone(models.Model):
    name = models.TextField(primary_key=True)
    due = models.BigIntegerField(blank=True, null=True)
    completed = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    product = models.ForeignKey(
        Product,
        db_column="product",
        on_delete=models.PROTECT,
    )

    class Meta:
        db_table = 'milestone'
        unique_together = (('name', 'product'),)


class Version(models.Model):
    name = models.TextField(primary_key=True)
    time = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    product = models.ForeignKey(
        Product,
        db_column="product",
        on_delete=models.PROTECT,
    )

    class Meta:
        db_table = 'version'
        unique_together = (('name', 'product'),)


class Ticket(models.Model):
    uid = models.AutoField(primary_key=True)
    type = models.ForeignKey(
        Enum,
        on_delete=models.PROTECT,
        db_column="type",
        related_name='%(app_label)s_%(class)s_type_related',
        blank=True,
        null=True,
    )
    time = models.BigIntegerField(blank=True, null=True)
    changetime = models.BigIntegerField(blank=True, null=True)
    component = models.ForeignKey(
        Component,
        on_delete=models.PROTECT,
        db_column="component",
        blank=True,
        null=True,
    )
    severity = models.TextField(blank=True, null=True)
    priority = models.TextField(blank=True, null=True)
    owner = models.TextField(blank=True, null=True)
    reporter = models.TextField(blank=True, null=True)
    cc = models.TextField(blank=True, null=True)
    version = models.ForeignKey(
        Version,
        on_delete=models.PROTECT,
        db_column="version",
        blank=True,
        null=True,
    )
    milestone = models.ForeignKey(
        Milestone,
        on_delete=models.PROTECT,
        db_column="milestone",
        blank=True,
        null=True,
    )
    status = models.TextField(blank=True, null=True)
    resolution = models.ForeignKey(
        Enum,
        on_delete=models.PROTECT,
        db_column="resolution",
        related_name='%(app_label)s_%(class)s_resolution_related',
        blank=True,
        null=True,
    )
    summary = models.TextField()
    description = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, db_column="product")
    product_ticket_id = models.IntegerField(db_column='id', editable=False)

    class Meta:
        db_table = 'ticket'
        unique_together = (('product', 'product_ticket_id'),)

    def save(self, *args, **kwargs):
        if self._state.adding:
            # FIXME: deleting the latest tickets will allow reuse
            # Consider:
            #     disallowing deletion
            #     switching to uuids
            #     recording last used on product model
            product_tickets = Ticket.objects.filter(product=self.product)
            if product_tickets.exists():
                newest = product_tickets.latest('product_ticket_id')
                new_id = 1 + newest.product_ticket_id
            else:
                new_id = 1
            self.product_ticket_id = new_id
        super().save(*args, **kwargs)


class TicketChange(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.PROTECT,
        db_column='ticket',
        related_name='%(app_label)s_%(class)s_ticket_related',
    )
    time = models.BigIntegerField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    field = models.TextField()
    oldvalue = models.TextField(blank=True, null=True)
    newvalue = models.TextField(blank=True, null=True)
    product = models.ForeignKey(
        Product,
        db_column="product",
        on_delete=models.PROTECT,
    )

    class Meta:
        db_table = 'ticket_change'
        unique_together = (('ticket', 'time', 'field', 'product'),)


class TicketCustom(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.PROTECT)
    name = models.TextField()
    value = models.TextField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    class Meta:
        db_table = 'ticket_custom'
        unique_together = (('ticket', 'name', 'product'),)


class Report(models.Model):
    author = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    query = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    class Meta:
        db_table = 'report'
        unique_together = (('id', 'product'),)
