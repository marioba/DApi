from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Data


class DataApiTest(APITestCase):

    def test_post_data(self):
        # Post data
        # test is present in the db correctly

        client = APIClient()
        response = client.post('/data/1/2', {'text': 'Start at the end and work back.', 'language': 'EN'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Data.objects.all()), 1)

        data  = Data.objects.all()[0]
        self.assertEqual(data.customer_id, 1)
        self.assertEqual(data.dialog_id, 2)
        self.assertEqual(data.language, 'EN')
        self.assertEqual(data.text, 'Start at the end and work back.')


    def test_get_data(self):
        # create 3 data
        # - user 1 lang EN
        # - user 1 lang IT
        # - user 2 lang EN
        # - user 2 lang EN without consent

        # test get all
        # test get user 1
        # test get lang EN
        # test get user 1 lang EN

        # test pagination
        # test sorted by most recent first


        Data.objects.create(
            customer_id=1,
            dialog_id=1,
            text="Hello",
            language="EN",
            consent=True,
        )

        Data.objects.create(
            customer_id=1,
            dialog_id=2,
            text="Ciao",
            language="IT",
            consent=True,
        )

        Data.objects.create(
            customer_id=2,
            dialog_id=3,
            text="Hi",
            language="EN",
            consent=True,
        )

        Data.objects.create(
            customer_id=2,
            dialog_id=4,
            text="Bye",
            language="EN",
            consent=False,
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
        Data.objects.create(
            customer_id=1,
            dialog_id=1,
            text="First",
            language="EN",
            consent=True,
        )

        Data.objects.create(
            customer_id=1,
            dialog_id=2,
            text="Second",
            language="IT",
            consent=True,
        )

        client = APIClient()
        response = client.get('/data/')
        self.assertEqual(len(response.data.get('results')), 2)
        results = response.data.get('results')
        self.assertEqual(results[0].get('text'), 'Second')
        self.assertEqual(results[1].get('text'), 'First')

    def test_get_data_pagination(self):
        for i in range(120):
            Data.objects.create(
                customer_id=1,
                dialog_id=i,
                text="hello",
                language="IT",
                consent=True,
            )

        client = APIClient()
        response = client.get('/data/')
        self.assertEqual(len(response.data.get('results')), 100)

        response = client.get('/data/?page=2')
        self.assertEqual(len(response.data.get('results')), 20)

    def test_post_consents(self):

        Data.objects.create(
            customer_id=1,
            dialog_id=1,
            text="hello",
            language="EN",
        )

        self.assertEqual(len(Data.objects.all()), 1)
        self.assertEqual(Data.objects.all()[0].consent, False)

        client = APIClient()
        response = client.post('/consents/1', {'consent': 'true'})

        self.assertEqual(len(Data.objects.all()), 1)
        self.assertEqual(Data.objects.all()[0].consent, True)

        response = client.post('/consents/1', {'consent': 'false'})

        self.assertEqual(len(Data.objects.all()), 0)
