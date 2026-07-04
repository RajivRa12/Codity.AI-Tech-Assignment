"""
Queue API tests — CRUD, pause, resume, stats.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import User
from projects.models import Organization, Project
from queues.models import Queue


class QueueTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create user and authenticate
        self.user = User.objects.create_user(username='quser', password='testpass123', email='q@test.com')
        self.admin = User.objects.create_user(username='qadmin', password='testpass123', email='qa@test.com', role='admin')
        # Create organization and project
        self.org = Organization.objects.create(name='TestOrg', owner=self.user)
        self.project = Project.objects.create(name='TestProject', organization=self.org, created_by=self.user)
        # Login
        login_resp = self.client.post(reverse('auth-login'), {'username': 'quser', 'password': 'testpass123'})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_resp.data['access']}")

    def _queue_data(self, name='MyQueue'):
        return {
            'name': name,
            'project': str(self.project.id),
            'description': 'A test queue',
            'priority': 5,
            'concurrency_limit': 2,
        }

    def test_create_queue(self):
        response = self.client.post('/api/queues/', self._queue_data())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'MyQueue')

    def test_list_queues(self):
        Queue.objects.create(project=self.project, name='Q1', concurrency_limit=1)
        Queue.objects.create(project=self.project, name='Q2', concurrency_limit=1)
        response = self.client.get('/api/queues/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 2)

    def test_pause_queue(self):
        q = Queue.objects.create(project=self.project, name='PQ', concurrency_limit=1)
        response = self.client.post(f'/api/queues/{q.id}/pause/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        q.refresh_from_db()
        self.assertTrue(q.is_paused)

    def test_resume_queue(self):
        q = Queue.objects.create(project=self.project, name='RQ', concurrency_limit=1, is_paused=True)
        response = self.client.post(f'/api/queues/{q.id}/resume/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        q.refresh_from_db()
        self.assertFalse(q.is_paused)

    def test_queue_stats(self):
        q = Queue.objects.create(project=self.project, name='SQ', concurrency_limit=1)
        response = self.client.get(f'/api/queues/{q.id}/stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('by_status', response.data)
        self.assertIn('total_jobs', response.data)

    def test_delete_queue(self):
        q = Queue.objects.create(project=self.project, name='DQ', concurrency_limit=1)
        response = self.client.delete(f'/api/queues/{q.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
