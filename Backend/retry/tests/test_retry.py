"""
Retry app tests — policy computation and schedule_retry logic.
"""
from django.test import TestCase
from retry.models import RetryPolicy
from retry.services import compute_next_delay


class RetryPolicyTest(TestCase):

    def _make_policy(self, policy_type, initial=60, backoff=2.0, max_retries=3):
        return RetryPolicy(
            name=f'test-{policy_type}',
            policy_type=policy_type,
            initial_delay_seconds=initial,
            backoff_factor=backoff,
            max_retries=max_retries
        )

    def test_fixed_delay_always_same(self):
        policy = self._make_policy('fixed', initial=30)
        self.assertEqual(compute_next_delay(policy, 1), 30)
        self.assertEqual(compute_next_delay(policy, 2), 30)
        self.assertEqual(compute_next_delay(policy, 5), 30)

    def test_linear_delay_grows_linearly(self):
        policy = self._make_policy('linear', initial=10)
        self.assertEqual(compute_next_delay(policy, 1), 10)
        self.assertEqual(compute_next_delay(policy, 2), 20)
        self.assertEqual(compute_next_delay(policy, 3), 30)

    def test_exponential_delay_doubles(self):
        policy = self._make_policy('exponential', initial=10, backoff=2.0)
        self.assertEqual(compute_next_delay(policy, 1), 10)   # 10 * 2^0
        self.assertEqual(compute_next_delay(policy, 2), 20)   # 10 * 2^1
        self.assertEqual(compute_next_delay(policy, 3), 40)   # 10 * 2^2

    def test_exponential_custom_backoff(self):
        policy = self._make_policy('exponential', initial=5, backoff=3.0)
        self.assertEqual(compute_next_delay(policy, 1), 5)    # 5 * 3^0
        self.assertEqual(compute_next_delay(policy, 2), 15)   # 5 * 3^1

    def test_unknown_policy_type_falls_back_to_initial(self):
        policy = self._make_policy('fixed', initial=45)
        policy.policy_type = 'unknown'
        self.assertEqual(compute_next_delay(policy, 1), 45)

    def test_retry_policy_creation(self):
        policy = RetryPolicy.objects.create(
            name='my-policy',
            policy_type='exponential',
            initial_delay_seconds=60,
            backoff_factor=2.0,
            max_retries=5
        )
        self.assertEqual(str(policy), 'my-policy')
        self.assertEqual(policy.max_retries, 5)
