from rest_framework import serializers
from .models import Job, JobExecution, ScheduledJob
from django.utils import timezone

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id','queue','type','payload','status','scheduled_at','cron','batch_id','attempts','max_retries','retry_policy','claimed_by','started_at','finished_at','result','error_message','created_by','created_at')
        read_only_fields = ('id','status','attempts','claimed_by','started_at','finished_at','result','error_message','created_by','created_at')

    def validate(self, attrs):
        jtype = attrs.get('type', 'immediate')
        if jtype == 'delayed' and not attrs.get('scheduled_at'):
            raise serializers.ValidationError({'scheduled_at':'scheduled_at required for delayed jobs'})
        if jtype == 'recurring' and not attrs.get('cron'):
            raise serializers.ValidationError({'cron':'cron expression required for recurring jobs'})
        return attrs

class CreateJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('queue','type','payload','scheduled_at','cron','batch_id','max_retries','retry_policy')

class JobExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobExecution
        fields = '__all__'

class ScheduledJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledJob
        fields = '__all__'
        read_only_fields = ('id','last_run_at','next_run_at')

    def validate_cron(self, value):
        # basic sanity; cron validation can be improved with croniter
        if not value:
            raise serializers.ValidationError('cron expression required')
        return value
