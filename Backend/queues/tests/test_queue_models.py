from django.test import TestCase
from django.contrib.auth import get_user_model
from projects.models import Organization, Project
from queues.models import Queue

User = get_user_model()

class QueueModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='pass')
        self.org = Organization.objects.create(name='o1', owner=self.user)
        self.project = Project.objects.create(name='p1', organization=self.org, created_by=self.user)

    def test_create_queue(self):
        q = Queue.objects.create(project=self.project, name='q1')
        self.assertEqual(q.name, 'q1')
        self.assertFalse(q.is_paused)
