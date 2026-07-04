from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from projects.models import Organization, Project
from queues.models import Queue

User = get_user_model()

class SchedulingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='apiuser', password='pass')
        self.org = Organization.objects.create(name='o', owner=self.user)
        self.project = Project.objects.create(name='p', organization=self.org, created_by=self.user)
        self.queue = Queue.objects.create(project=self.project, name='q')
        self.client.force_authenticate(self.user)

    def test_create_schedule(self):
        resp = self.client.post('/api/scheduling/schedules/', {'project': str(self.project.id), 'name':'s1','cron':'*/5 * * * *'}, format='json')
        self.assertIn(resp.status_code, (200,201))
