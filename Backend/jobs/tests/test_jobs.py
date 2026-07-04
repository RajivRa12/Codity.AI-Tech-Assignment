"""
Job API tests — create (immediate, delayed, scheduled, recurring, batch), cancel, retry.
"""
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import User
from projects.models import Organization, Project
from queues.models import Queue
from jobs.models import Job
import datetime


class JobTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='jobuser', password='testpass123', email='j@test.com')
        self.org = Organization.objects.create(name='JobOrg', owner=self.user)
        self.project = Project.objects.create(name='JobProject', organization=self.org, created_by=self.user)
        self.queue = Queue.objects.create(project=self.project, name='MainQ', concurrency_limit=4)
        login = self.client.post(reverse('auth-login'), {'username': 'jobuser', 'password': 'testpass123'})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")

    def _job_base(self, **overrides):
        data = {
            'queue': str(self.queue.id),
            'payload': {'task': 'send_email', 'to': 'user@example.com'},
            'type': 'immediate',
        }
        data.update(overrides)
        return data

    # ── Create Jobs ───────────────────────────────────────────────────────────
    def test_create_immediate_job(self):
        resp = self.client.post('/api/jobs/', self._job_base(), format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['status'], 'queued')
        self.assertEqual(resp.data['type'], 'immediate')

    def test_create_delayed_job(self):
        future = (timezone.now() + datetime.timedelta(minutes=10)).isoformat()
        resp = self.client.post('/api/jobs/create_delayed/', self._job_base(scheduled_at=future), format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_create_scheduled_job(self):
        future = (timezone.now() + datetime.timedelta(hours=1)).isoformat()
        resp = self.client.post('/api/jobs/create_scheduled/', self._job_base(scheduled_at=future), format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_create_recurring_job(self):
        resp = self.client.post('/api/jobs/create_recurring/', self._job_base(cron='*/5 * * * *'), format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_create_batch_jobs(self):
        jobs = [self._job_base(payload={'i': i}) for i in range(3)]
        resp = self.client.post('/api/jobs/create_batch/', {'jobs': jobs}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(resp.data), 3)

    # ── Cancel ────────────────────────────────────────────────────────────────
    def test_cancel_queued_job(self):
        job = Job.objects.create(queue=self.queue, type='immediate', status='queued', created_by=self.user)
        resp = self.client.post(f'/api/jobs/{job.id}/cancel/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        job.refresh_from_db()
        self.assertEqual(job.status, 'dead')

    def test_cancel_completed_job_fails(self):
        job = Job.objects.create(queue=self.queue, type='immediate', status='completed', created_by=self.user)
        resp = self.client.post(f'/api/jobs/{job.id}/cancel/')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # ── Retry ─────────────────────────────────────────────────────────────────
    def test_retry_failed_job(self):
        job = Job.objects.create(queue=self.queue, type='immediate', status='failed', attempts=1, max_retries=3, created_by=self.user)
        resp = self.client.post(f'/api/jobs/{job.id}/retry/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_retry_exceeds_max_retries(self):
        job = Job.objects.create(queue=self.queue, type='immediate', status='failed', attempts=3, max_retries=3, created_by=self.user)
        resp = self.client.post(f'/api/jobs/{job.id}/retry/')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # ── List + Filter ─────────────────────────────────────────────────────────
    def test_list_jobs_returns_paginated(self):
        for i in range(5):
            Job.objects.create(queue=self.queue, type='immediate', status='queued', created_by=self.user)
        resp = self.client.get('/api/jobs/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('results', resp.data)

    def test_jobs_require_auth(self):
        self.client.credentials()
        resp = self.client.get('/api/jobs/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
