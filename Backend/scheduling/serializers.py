from rest_framework import serializers
from .models import Schedule, ScheduleExecution
import croniter

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'
        read_only_fields = ('id','last_run_at','next_run_at','created_at','updated_at')

    def validate_cron(self, value):
        if not croniter.croniter.is_valid(value):
            raise serializers.ValidationError("Invalid cron expression format.")
        return value

class ScheduleExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleExecution
        fields = '__all__'
        read_only_fields = ('id','created_at')
