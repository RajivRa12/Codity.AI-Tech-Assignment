"""
Worker app tests — registration, heartbeat, stale detection.
"""
from django.test import TestCase
from django.utils import timezone
import datetime
from workers.models import Worker, WorkerHeartbeat
from workers.services import register_worker, detect_stale_workers


class WorkerServiceTest(TestCase):

    def test_register_worker_creates(self):
        worker = register_worker(name='w1', hostname='host1', pid=1234, concurrency=4)
        self.assertIsNotNone(worker.id)
        self.assertEqual(worker.name, 'w1')
        self.assertEqual(worker.status, 'online')

    def test_register_worker_idempotent(self):
        w1 = register_worker(name='idempotent-worker', hostname='h1', concurrency=1)
        w2 = register_worker(name='idempotent-worker', hostname='h1', concurrency=1)
        self.assertEqual(w1.id, w2.id)
        self.assertEqual(Worker.objects.filter(name='idempotent-worker').count(), 1)

    def test_heartbeat_creates_record(self):
        worker = register_worker(name='hw', hostname='h1', concurrency=1)
        initial_count = WorkerHeartbeat.objects.filter(worker=worker).count()
        worker.last_heartbeat = timezone.now()
        worker.save()
        WorkerHeartbeat.objects.create(worker=worker, meta={'cpu': 0.5})
        self.assertEqual(WorkerHeartbeat.objects.filter(worker=worker).count(), initial_count + 1)

    def test_detect_stale_workers(self):
        stale_worker = Worker.objects.create(
            name='stale',
            hostname='h2',
            status='online',
            last_heartbeat=timezone.now() - datetime.timedelta(minutes=5)
        )
        fresh_worker = Worker.objects.create(
            name='fresh',
            hostname='h3',
            status='online',
            last_heartbeat=timezone.now()
        )
        stale = list(detect_stale_workers(timeout_seconds=60))
        stale_ids = [w.id for w in stale]
        self.assertIn(stale_worker.id, stale_ids)
        self.assertNotIn(fresh_worker.id, stale_ids)

    def test_worker_str(self):
        w = Worker(name='test', hostname='myhost')
        self.assertIn('test', str(w))
