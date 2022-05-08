from rest_framework import serializers

from dataapi.core.models import Dialog, Consent


class DialogSerializer(serializers.ModelSerializer):

    # TODO: comment
    customerId = serializers.IntegerField(source="customer_id")
    dialogId = serializers.IntegerField(source="dialog_id")

    class Meta:
        model = Dialog
        fields = ['customerId', 'dialogId', 'text', 'language']


class ConsentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consent
        fields = ['dialog', 'approved']
