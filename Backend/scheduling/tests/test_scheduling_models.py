from django.test import TestCase
from django.contrib.auth import get_user_model
from projects.models import Organization, Project
from queues.models import Queue
from scheduling.models import Schedule

User = get_user_model()

class SchedulingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='pass')
        org = Organization.objects.create(name='o1', owner=self.user)
        self.project = Project.objects.create(name='p1', organization=org, created_by=self.user)
        self.queue = Queue.objects.create(project=self.project, name='q1')

    def test_create_schedule(self):
        s = Schedule.objects.create(project=self.project, name='s1', cron='*/5 * * * *', created_by=self.user)
        self.assertEqual(s.name, 's1')
