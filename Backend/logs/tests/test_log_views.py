from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class LogsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='apiuser', password='pass')
        self.client.force_authenticate(self.user)

    def test_list_logs(self):
        resp = self.client.get('/api/logs/logs/')
        self.assertEqual(resp.status_code, 200)
