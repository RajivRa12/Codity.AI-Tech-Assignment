from django.contrib import admin
from .models import Worker, WorkerHeartbeat

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name','hostname','pid','concurrency','status','last_heartbeat')
    list_filter = ('status',)
    search_fields = ('name','hostname')

@admin.register(WorkerHeartbeat)
class WorkerHeartbeatAdmin(admin.ModelAdmin):
    list_display = ('worker','seen_at')
    list_filter = ('seen_at',)
