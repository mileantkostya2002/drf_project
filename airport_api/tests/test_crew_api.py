from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from airport_api.models import Crew

from airport_api.serializers import CrewSerializer

CREW_URL = reverse('airport-api:crew-list')

def sample_crew(**params):
    defaults = {
        'first_name': 'Brad',
        'last_name': 'Pitt'
    }
    defaults.update(params)
    return Crew.objects.create(**defaults)





class UnauthenticatedCrewApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(CREW_URL)
        self.assertEqual(
            res.status_code,
            status.HTTP_401_UNAUTHORIZED
        )


class AuthenticatedCrewApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="<PASSWORD>"
        )
        self.client.force_authenticate(self.user)

    def test_get_list_of_crew(self):
        sample_crew()

        crews = Crew.objects.all()
        serializer = CrewSerializer(crews, many=True)

        res = self.client.get(CREW_URL)
        self.assertEqual(res.data["results"], serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_crew_forbidden(self):
        payload = {
            "first_name": "Brad",
            "last_name": "Pitt",
        }
        res = self.client.post(CREW_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

class AdminUserCrewApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="<PASSWORD>",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_crew(self):
        payload = {
            "first_name": "Brad",
            "last_name": "Pitt",
        }
        res = self.client.post(CREW_URL, payload)
        crew = Crew.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        for key in payload:
            self.assertEqual(payload[key], getattr(crew, key))

    def test_retrieve_crew(self):
        sample_crew()

        res = self.client.get(f"{CREW_URL}1/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_crew(self):
        sample_crew()

        res = self.client.put(f"{CREW_URL}1/", {"first_name": "Jim"})
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_crew(self):
        sample_crew()

        res = self.client.delete(f"{CREW_URL}1/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)