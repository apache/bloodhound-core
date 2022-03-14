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

from django.urls import path
from django.conf.urls import include
from rest_framework.schemas import get_schema_view
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('groups', views.GroupViewSet)
router.register('products', views.ProductViewSet)

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('tickets', views.TicketViewSet, basename='product-tickets')
products_router.register('components', views.ComponentViewSet, basename='product-components')
products_router.register('milestones', views.MilestoneViewSet, basename='product-milestones')
products_router.register('versions', views.VersionViewSet, basename='product-versions')
products_router.register('ticketchanges', views.TicketChangeViewSet, basename='product-ticketchanges')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('openapi', get_schema_view(
        title="Apache Bloodhound",
        version="0.1.0",
    ), name='openapi-schema'),
    path(
        'swagger<str:format>',
        views.schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    path(
        'swagger/',
        views.schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    path(
        'redoc/',
        views.schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
]
