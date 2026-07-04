from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class WorkerAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='apiuser', password='pass')
        self.client.force_authenticate(self.user)

    def test_register_worker(self):
        resp = self.client.post('/api/workers/workers/register/', {'name':'w1','hostname':'h1','pid':123})
        self.assertIn(resp.status_code, (200,201))
