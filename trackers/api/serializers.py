from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.reverse import reverse
from ..models import (
    Component,
    Milestone,
    Product,
    Ticket,
    TicketChange,
    Version,
)
from functools import partial


def get_self_url(obj, context, obj_type):
    keywords = {
        'product_prefix': obj.product.prefix,
    }
    if obj_type == 'ticket':
        keywords['product_ticket_id'] = obj.product_ticket_id
    elif obj_type == 'ticketchange':
        keywords['time'] = obj.time
    else:
        keywords['name'] = obj.name

    return reverse(
        f'product-{obj_type}s-detail',
        kwargs=keywords,
        request=context['request'],
    )


class ProductChildSerializer(serializers.HyperlinkedModelSerializer):
    product_url = serializers.SerializerMethodField()

    def get_product_url(self, obj):
        keywords = {
            'prefix': obj.product.prefix,
        }
        return reverse(
            'product-detail',
            kwargs=keywords,
            request=self.context['request']
        )

    def create(self, validated_data):
        if 'prefix' not in self.context['view'].kwargs.keys():
            prefix = self.context['view'].kwargs['product_prefix']
            product = get_object_or_404(Product.objects.all(), prefix=prefix)
            validated_data['product'] = product
        return super().create(validated_data)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class TicketChangeSerializer(ProductChildSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = TicketChange
        fields = ('url', 'time', 'author', 'field', 'oldvalue', 'newvalue')

    def get_url(self, obj):
        return get_self_url(obj, self.context, 'ticketchange')


class TicketSerializer(ProductChildSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = (
            'product_url',
            'url',
            'product_ticket_id',
            'summary',
            'description',
            'time',
            'changetime',
            'reporter',
            'owner',
            'cc',
            'status',
            'severity',
            'priority',
            'keywords',
        )
        extra_kwargs = {
            'product_ticket_id': {'required': False},
        }

    def get_url(self, obj):
        return get_self_url(obj, self.context, 'ticket')


class ComponentSerializer(ProductChildSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Component
        fields = (
            'product_url',
            'url',
            'name',
            'description',
            'owner',
        )

    def get_url(self, obj):
        return get_self_url(obj, self.context, 'component')


class MilestoneSerializer(ProductChildSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Milestone
        fields = (
            'product_url',
            'url',
            'name',
            'description',
            'due',
            'completed',
        )

    def get_url(self, obj):
        return get_self_url(obj, self.context, 'milestone')


class VersionSerializer(ProductChildSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Version
        fields = (
            'product_url',
            'url',
            'name',
            'description',
            'time',
        )

    def get_url(self, obj):
        return get_self_url(obj, self.context, 'version')


ProductHyperlinkedModelSerializer = partial(
    serializers.HyperlinkedIdentityField,
    lookup_field='prefix',
    lookup_url_kwarg='product_prefix',
)


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='prefix',
    )
    tickets_url = ProductHyperlinkedModelSerializer(
        view_name='product-tickets-list',
    )
    components_url = ProductHyperlinkedModelSerializer(
        view_name='product-components-list',
    )
    milestones_url = ProductHyperlinkedModelSerializer(
        view_name='product-milestones-list',
    )
    versions_url = ProductHyperlinkedModelSerializer(
        view_name='product-versions-list',
    )

    ticketchanges_url = ProductHyperlinkedModelSerializer(
        view_name='product-ticketchanges-list',
    )

    class Meta:
        model = Product
        fields = (
            'url',
            'prefix',
            'name',
            'description',
            'owner',
            'tickets_url',
            'components_url',
            'milestones_url',
            'versions_url',
            'ticketchanges_url',
        )
