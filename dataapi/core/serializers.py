from rest_framework import serializers

from dataapi.core.models import Data


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ['customer_id', 'dialog_id', 'text', 'language']

