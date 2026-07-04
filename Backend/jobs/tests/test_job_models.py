from django.test import TestCase
from django.contrib.auth import get_user_model
from projects.models import Organization, Project
from queues.models import Queue
from jobs.models import Job

User = get_user_model()

class JobModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='pass')
        org = Organization.objects.create(name='o1', owner=self.user)
        project = Project.objects.create(name='p1', organization=org, created_by=self.user)
        self.queue = Queue.objects.create(project=project, name='q1')

    def test_create_immediate_job(self):
        job = Job.objects.create(queue=self.queue, type='immediate', payload={'a':1}, created_by=self.user)
        self.assertEqual(job.status, 'queued')
