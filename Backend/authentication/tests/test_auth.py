"""
Authentication app tests — register, login, refresh, logout, me, change-password.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import User


class AuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('auth-register')
        self.login_url = reverse('auth-login')
        self.logout_url = reverse('auth-logout')
        self.me_url = reverse('auth-me')
        self.change_password_url = reverse('auth-change-password')

    def _register_user(self, username='testuser', password='testpass123'):
        data = {'username': username, 'email': f'{username}@example.com', 'password': password}
        return self.client.post(self.register_url, data)

    def _login_user(self, username='testuser', password='testpass123'):
        return self.client.post(self.login_url, {'username': username, 'password': password})

    # ── Register ──────────────────────────────────────────────────────────────
    def test_register_success(self):
        response = self._register_user()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_duplicate_username(self):
        self._register_user()
        response = self._register_user()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_missing_password(self):
        response = self.client.post(self.register_url, {'username': 'nopass', 'email': 'a@b.com'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ── Login ─────────────────────────────────────────────────────────────────
    def test_login_success(self):
        self._register_user()
        response = self._login_user()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_wrong_password(self):
        self._register_user()
        response = self._login_user(password='wrongpassword')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ── Me ────────────────────────────────────────────────────────────────────
    def test_me_requires_auth(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_returns_user(self):
        self._register_user()
        tokens = self._login_user().data
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    # ── Password Change ───────────────────────────────────────────────────────
    def test_change_password_success(self):
        self._register_user()
        tokens = self._login_user().data
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        response = self.client.post(self.change_password_url, {
            'old_password': 'testpass123',
            'new_password': 'newpassword456'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password_wrong_old(self):
        self._register_user()
        tokens = self._login_user().data
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        response = self.client.post(self.change_password_url, {
            'old_password': 'WRONGOLD',
            'new_password': 'newpassword456'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ── Logout ────────────────────────────────────────────────────────────────
    def test_logout_success(self):
        self._register_user()
        tokens = self._login_user().data
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        response = self.client.post(self.logout_url, {'refresh': tokens['refresh']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_without_refresh_token(self):
        self._register_user()
        tokens = self._login_user().data
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        response = self.client.post(self.logout_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
