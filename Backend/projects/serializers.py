from rest_framework import serializers
from .models import Organization, Project


class OrganizationSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Organization
        fields = ('id', 'name', 'description', 'owner', 'owner_username', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'owner', 'owner_username', 'created_at', 'updated_at')


class ProjectSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    queue_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            'id', 'name', 'description', 'organization', 'organization_name',
            'created_by', 'created_by_username', 'is_active',
            'queue_count', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_by', 'created_by_username', 'created_at', 'updated_at')

    def get_queue_count(self, obj):
        return obj.queues.count()


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'organization', 'is_active')
        read_only_fields = ('id',)
