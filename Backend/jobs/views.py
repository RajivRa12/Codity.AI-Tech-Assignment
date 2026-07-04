from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from .models import Job, JobExecution, ScheduledJob
from .serializers import JobSerializer, CreateJobSerializer, JobExecutionSerializer, ScheduledJobSerializer
from .permissions import IsQueueOwnerOrAdmin
from .services import enqueue_job, claim_next_job, mark_running, mark_completed, mark_failed
from django.utils import timezone

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['payload']
    ordering_fields = ['created_at','scheduled_at']

    def get_serializer_class(self):
        if self.action == 'create' or self.action in ['create_immediate','create_delayed','create_scheduled','create_recurring','create_batch']:
            return CreateJobSerializer
        return JobSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job = serializer.save(created_by=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(JobSerializer(job).data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['post'])
    def create_immediate(self, request):
        serializer = CreateJobSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        job = serializer.save(created_by=request.user)
        return Response(JobSerializer(job).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def create_delayed(self, request):
        data = request.data.copy()
        data['type'] = 'delayed'
        serializer = CreateJobSerializer(data=data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        job = serializer.save(created_by=request.user)
        return Response(JobSerializer(job).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def create_scheduled(self, request):
        data = request.data.copy()
        data['type'] = 'scheduled'
        serializer = CreateJobSerializer(data=data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        job = serializer.save(created_by=request.user)
        return Response(JobSerializer(job).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def create_recurring(self, request):
        data = request.data.copy()
        data['type'] = 'recurring'
        serializer = CreateJobSerializer(data=data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        job = serializer.save(created_by=request.user)
        return Response(JobSerializer(job).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def create_batch(self, request):
        jobs = []
        for item in request.data.get('jobs', []):
            item['type'] = 'batch'
            serializer = CreateJobSerializer(data=item, context={'request':request})
            serializer.is_valid(raise_exception=True)
            job = serializer.save(created_by=request.user)
            jobs.append(job)
        return Response(JobSerializer(jobs, many=True).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        job = self.get_object()
        if job.status in ['completed','dead']:
            return Response({'detail':'cannot cancel'}, status=status.HTTP_400_BAD_REQUEST)
        job.status = 'dead'
        job.save()
        return Response({'status':'cancelled'})

    @action(detail=True, methods=['post'])
    def retry(self, request, pk=None):
        job = self.get_object()
        from .services import retry_job
        ok = retry_job(job)
        if ok:
            return Response({'status':'requeued'})
        return Response({'status':'max_retries_exceeded'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def claim(self, request, pk=None):
        # manual claim for debugging
        job = self.get_object()
        job.status = 'claimed'
        job.claimed_by = None
        job.locked_at = timezone.now()
        job.attempts += 1
        job.save()
        return Response(JobSerializer(job).data)

class JobExecutionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JobExecution.objects.all()
    serializer_class = JobExecutionSerializer
    permission_classes = (permissions.IsAuthenticated,)

class ScheduledJobViewSet(viewsets.ModelViewSet):
    queryset = ScheduledJob.objects.all()
    serializer_class = ScheduledJobSerializer
    permission_classes = (permissions.IsAuthenticated,)
