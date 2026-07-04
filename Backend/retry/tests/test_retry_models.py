from django.test import TestCase
from retry.models import RetryPolicy

class RetryModelTest(TestCase):
    def test_create_policy(self):
        p = RetryPolicy.objects.create(name='p1', policy_type='fixed', initial_delay_seconds=10, max_retries=2)
        self.assertEqual(p.name, 'p1')
