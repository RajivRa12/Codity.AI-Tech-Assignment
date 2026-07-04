from rest_framework import serializers
from .models import Worker, WorkerHeartbeat

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ('id','name','hostname','pid','concurrency','status','last_heartbeat','registered_at')
        read_only_fields = ('id','last_heartbeat','registered_at')

class HeartbeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerHeartbeat
        fields = ('id','worker','seen_at','meta')
        read_only_fields = ('id','seen_at')
