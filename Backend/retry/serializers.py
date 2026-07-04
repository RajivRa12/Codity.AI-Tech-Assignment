from rest_framework import serializers
from .models import RetryPolicy, RetryAttempt

class RetryPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = RetryPolicy
        fields = '__all__'
        read_only_fields = ('id','created_at','updated_at')

class RetryAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetryAttempt
        fields = '__all__'
        read_only_fields = ('id','created_at','executed_at')
