from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from ..models import Product, Ticket


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            'product_ticket_id',
            'summary',
            'description',
        )
        extra_kwargs = {'product_ticket_id': {'required': False}}

    def create(self, validated_data):
        if 'prefix' not in self.context['view'].kwargs.keys():
            prefix = self.context['view'].kwargs['product_prefix']
            product = get_object_or_404(Product.objects.all(), prefix=prefix)
            validated_data['product'] = product
        return super().create(validated_data)
