from rest_framework import generics, status
from rest_framework.response import Response

from dataapi.core.models import Dialog, Consent
from dataapi.core.serializers import DialogSerializer, ConsentSerializer


class CreateDataView(generics.CreateAPIView):
    """View class to manage POST `data/` endpoint"""

    serializer_class = DialogSerializer

    # The serializers in django rest framework, expect to find all the
    # fields to create an object in the body of the request. Here we
    # copy the parameters received via path params into the request
    # data.
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data.update({'customerId': kwargs['customerId'], 'dialogId': kwargs['dialogId']})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ListDataView(generics.ListAPIView):
    """View class to manage GET `data/` endpoint"""

    serializer_class = DialogSerializer

    # We override the get_queryset method to implement the filters
    # defined by the query params
    def get_queryset(self):
        queryset = Dialog.objects.filter(consent__approved=True).order_by('-created_at')

        language = self.request.query_params.get('language', None)
        if language is not None:
            queryset = queryset.filter(language=language)

        customer_id = self.request.query_params.get('customerId', None)
        if customer_id is not None:
            queryset = queryset.filter(customer_id=customer_id)

        return queryset


class ConsentsView(generics.CreateAPIView):
    """View class to manage `consents/` endpoints"""

    serializer_class = ConsentSerializer

    # The serializers in django rest framework, expect to find all the
    # fields to create an object in the body of the request. Here we
    # copy the parameters received via path params into the request
    # data.
    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # If the user doesn't give the consent, the dialog's data is
        # deleted
        if data.get('approved', '').lower() == 'false':
            Dialog.objects.get(dialog_id=kwargs['dialogId']).delete()
            return Response(status=status.HTTP_200_OK)
        data.update({'dialog': kwargs['dialogId']})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

