import signal
import threading
import time
import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from workers.services import register_worker, WorkerRunner
from workers.models import Worker
from queues.models import Queue

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Run worker dispatcher that polls queues and dispatches jobs to Celery'

    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, default='worker1')
        parser.add_argument('--concurrency', type=int, default=1)
        parser.add_argument('--poll-interval', type=int, default=5)
        parser.add_argument('--recover-delay', type=int, default=5)

    def handle(self, *args, **options):
        name = options['name']
        concurrency = options['concurrency']
        poll_interval = options['poll_interval']
        recover_delay = options['recover_delay']

        # register or update worker row
        worker = register_worker(name=name, hostname=None, pid=None, concurrency=concurrency)

        stop_event = threading.Event()

        def _signal_handler(signum, frame):
            logger.info('Received signal %s, initiating graceful shutdown', signum)
            worker.status = 'draining'
            worker.save(update_fields=['status'])
            stop_event.set()

        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)

        runner = WorkerRunner(worker=worker, poll_interval=poll_interval, stop_event=stop_event)

        # gather queues to poll
        def get_queues():
            return list(Queue.objects.all())

        logger.info('Worker %s started with concurrency=%s poll_interval=%s', name, concurrency, poll_interval)

        # Main loop with simple auto-recover
        while not stop_event.is_set():
            try:
                queues = get_queues()
                runner.run(queues, concurrency=concurrency)
            except Exception as exc:
                logger.exception('Worker runner crashed: %s. Recovering in %s seconds', exc, recover_delay)
                time.sleep(recover_delay)

        logger.info('Worker %s shutting down', name)
        worker.status = 'offline'
        worker.save(update_fields=['status','updated_at'])
