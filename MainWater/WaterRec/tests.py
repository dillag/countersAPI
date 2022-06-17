from django.test import TestCase
from ..WaterRec.models import Service_Record
from datetime import datetime
from django.contrib.auth.models import User

class Service_RecordTestCase(TestCase):
    def setUp(self):
        user = User.objects.get(username="dillag1")
        Service_Record.objects.create(user_id=user, service="Электрик", description="hohoho", DateTime=datetime.now())

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        user = User.objects.get(username="dillag1")
        our_service = Service_Record.objects.get(service="Электрик", user_id=user)

        self.assertEqual(our_service.description, 'hohoho')
# Create your tests here.
