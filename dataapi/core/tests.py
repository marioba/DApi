from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from dataapi.core.models import Dialog, Consent

# TODO: test wrong or missing values
class DataApiTest(APITestCase):

    def test_post_data(self):
        """Test POST `data/` endpoint"""
        client = APIClient()
        response = client.post('/data/1/2', {'text': 'Start at the end and work back.', 'language': 'EN'})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Dialog.objects.all()), 1)

        data  = Dialog.objects.all()[0]
        self.assertEqual(data.customer_id, 1)
        self.assertEqual(data.dialog_id, 2)
        self.assertEqual(data.language, 'EN')
        self.assertEqual(data.text, 'Start at the end and work back.')


    def test_get_data(self):
        """Test GET `data/` endpoint"""

        dialog = Dialog.objects.create(
            customer_id=1,
            dialog_id=1,
            text="Hello",
            language="EN",
        )
        Consent.objects.create(
            dialog=dialog,
            approved=True
        )

        dialog = Dialog.objects.create(
            customer_id=1,
            dialog_id=2,
            text="Ciao",
            language="IT",
        )
        Consent.objects.create(
            dialog=dialog,
            approved=True
        )

        dialog = Dialog.objects.create(
            customer_id=2,
            dialog_id=3,
            text="Hi",
            language="EN",
        )
        Consent.objects.create(
            dialog=dialog,
            approved=True
        )

        dialog = Dialog.objects.create(
            customer_id=2,
            dialog_id=4,
            text="Bye",
            language="EN",
        )
        Consent.objects.create(
            dialog=dialog,
            approved=False
        )

        client = APIClient()
        response = client.get('/data/')
        self.assertEqual(len(response.data.get('results')), 3)
        response = client.get('/data/?customerId=1')
        self.assertEqual(len(response.data.get('results')), 2)
        response = client.get('/data/?language=EN')
        self.assertEqual(len(response.data.get('results')), 2)
        response = client.get('/data/?customerId=1&language=EN')

    def test_get_data_order(self):
        """Test if GET `data/` endpoint's result is sorted"""
        dialog = Dialog.objects.create(
            customer_id=1,
            dialog_id=1,
            text="First",
            language="EN",
        )
        Consent.objects.create(
            dialog=dialog,
            approved=True
        )

        dialog = Dialog.objects.create(
            customer_id=1,
            dialog_id=2,
            text="Second",
            language="IT",
        )
        Consent.objects.create(
            dialog=dialog,
            approved=True
        )

        client = APIClient()
        response = client.get('/data/')
        self.assertEqual(len(response.data.get('results')), 2)
        results = response.data.get('results')
        self.assertEqual(results[0].get('text'), 'Second')
        self.assertEqual(results[1].get('text'), 'First')

    def test_get_data_pagination(self):
        """Test pagination on GET `data/` endpoint's result"""

        for i in range(120):
            dialog = Dialog.objects.create(
                customer_id=1,
                dialog_id=i,
                text="hello",
                language="IT",
            )
            Consent.objects.create(
                dialog=dialog,
                approved=True
            )

        client = APIClient()
        response = client.get('/data/')
        self.assertEqual(len(response.data.get('results')), 100)

        response = client.get('/data/?page=2')
        self.assertEqual(len(response.data.get('results')), 20)

    def test_post_consents(self):
        """Test POST `consents/` result"""

        dialog = Dialog.objects.create(
            customer_id=1,
            dialog_id=1,
            text="hello",
            language="EN",
        )

        self.assertEqual(len(Dialog.objects.all()), 1)
        self.assertEqual(len(Consent.objects.all()), 0)

        client = APIClient()
        response = client.post('/consents/1', {'approved': 'true'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Dialog.objects.all()), 1)
        self.assertEqual(len(Consent.objects.all()), 1)
        self.assertTrue(Consent.objects.all()[0].approved)
        self.assertEqual(Consent.objects.all()[0].dialog, dialog)

        response = client.post('/consents/1', {'approved': 'false'})
        self.assertEqual(len(Dialog.objects.all()), 0)
        self.assertEqual(len(Consent.objects.all()), 0)
