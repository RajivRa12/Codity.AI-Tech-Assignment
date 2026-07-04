from django.contrib import admin
from .models import Organization, Project


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'owner__username')
    ordering = ('-created_at',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'created_by', 'is_active', 'created_at')
    list_filter = ('is_active', 'organization')
    search_fields = ('name', 'description', 'created_by__username')
    ordering = ('-created_at',)
    raw_id_fields = ('organization', 'created_by')
