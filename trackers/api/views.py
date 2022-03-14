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

from django.contrib.auth.models import User, Group
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions, viewsets
from . import serializers
from .. import models


schema_view = get_schema_view(
    openapi.Info(
        title='Bloodhound Core API',
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    lookup_field = 'prefix'


class TicketChangeViewSet(viewsets.ModelViewSet):
    queryset = models.TicketChange.objects.all()
    serializer_class = serializers.TicketChangeSerializer
    lookup_field = 'time'

    def get_queryset(self, *args, **kwargs):
        prefix = self.kwargs['product_prefix']
        return models.TicketChange.objects.filter(product=prefix)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = models.Ticket.objects.all()
    serializer_class = serializers.TicketSerializer
    lookup_field = 'product_ticket_id'

    def get_queryset(self, *args, **kwargs):
        prefix = self.kwargs['product_prefix']
        return models.Ticket.objects.filter(product=prefix)


class ComponentViewSet(viewsets.ModelViewSet):
    queryset = models.Component.objects.all()
    serializer_class = serializers.ComponentSerializer
    lookup_field = 'name'
    lookup_value_regex = '[^/]+'

    def get_queryset(self, *args, **kwargs):
        prefix = self.kwargs['product_prefix']
        return models.Component.objects.filter(product=prefix)


class MilestoneViewSet(viewsets.ModelViewSet):
    queryset = models.Milestone.objects.all()
    serializer_class = serializers.MilestoneSerializer
    lookup_field = 'name'
    lookup_value_regex = '[^/]+'

    def get_queryset(self, *args, **kwargs):
        prefix = self.kwargs['product_prefix']
        return models.Milestone.objects.filter(product=prefix)


class VersionViewSet(viewsets.ModelViewSet):
    queryset = models.Version.objects.all()
    serializer_class = serializers.VersionSerializer
    lookup_field = 'name'
    lookup_value_regex = '[^/]+'

    def get_queryset(self, *args, **kwargs):
        prefix = self.kwargs['product_prefix']
        return models.Version.objects.filter(product=prefix)
