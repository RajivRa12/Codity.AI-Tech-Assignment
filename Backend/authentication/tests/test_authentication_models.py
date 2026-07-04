from django.test import TestCase
from authentication.models import User

class UserModelTest(TestCase):
    def test_create_user(self):
        u = User.objects.create_user(username='u1', password='pass')
        self.assertEqual(u.username, 'u1')
