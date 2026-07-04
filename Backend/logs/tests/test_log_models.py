from django.test import TestCase
from logs.models import LogEntry

class LogModelTest(TestCase):
    def test_create_log(self):
        l = LogEntry.objects.create(level='INFO', event_type='test', message='hello')
        self.assertEqual(l.event_type, 'test')
