from django.test import TestCase
from workers.models import Worker

class WorkerModelTest(TestCase):
    def test_create_worker(self):
        w = Worker.objects.create(name='w1', hostname='h1', pid=123)
        self.assertEqual(w.name, 'w1')
        self.assertEqual(w.hostname, 'h1')
