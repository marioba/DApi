from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from dataapi.core.models import Data
from dataapi.core.serializers import DataSerializer

class DataView(generics.ListCreateAPIView):
    serializer_class = DataSerializer

    def get_queryset(self):
        language = self.request.query_params.get('language', None)
        customerId = self.request.query_params.get('customerId', None)
        queryset = Data.objects.filter(consent=True).order_by('-created_at')

        if language:
            queryset = queryset.filter(language=language)

        if customerId:
            queryset = queryset.filter(customer_id=customerId)

        return queryset

    def post(self, request, customerId, dialogId):
        text = request.data.get('text', None)
        language = request.data.get('language', None)

        Data.objects.create(
            customer_id = customerId,
            dialog_id = dialogId,
            text = text,
            language = language
        )
        return Response()


class ConsentsView(APIView):

    def post(self, request, dialogId):

        data = Data.objects.get(dialog_id=dialogId)

        if request.data.get('consent', None) == 'true':
            data.consent = True
            data.save()
        else:
            data.delete()

        return Response()
