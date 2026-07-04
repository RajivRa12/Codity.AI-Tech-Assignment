from rest_framework import serializers
from .models import Queue

class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = ('id','project','name','description','priority','concurrency_limit','retry_policy','is_paused','created_at','updated_at')
        read_only_fields = ('id','created_at','updated_at')
