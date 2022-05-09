from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from dataapi.core.models import Dialog, Consent


class DialogSerializer(serializers.ModelSerializer):

    # Here we associate parameters with variable names that do not
    # match because of camelCase
    customerId = serializers.IntegerField(source="customer_id")
    dialogId = serializers.IntegerField(source="dialog_id")

    class Meta:
        model = Dialog
        fields = ['customerId', 'dialogId', 'text', 'language']

    def validate(self, data):
        if Dialog.objects.filter(dialog_id=data.get('dialog_id')).exists():
            raise ValidationError('DialogId already exists')
        return data

class ConsentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consent
        fields = ['dialog', 'approved']
