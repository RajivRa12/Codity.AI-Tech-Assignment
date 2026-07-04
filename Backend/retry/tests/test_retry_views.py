from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class RetryAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='apiuser', password='pass')
        self.client.force_authenticate(self.user)

    def test_create_policy(self):
        resp = self.client.post('/api/retry/policies/', {'name':'p1','policy_type':'fixed','initial_delay_seconds':10,'max_retries':2})
        self.assertIn(resp.status_code, (200,201))
