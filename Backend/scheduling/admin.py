from django.contrib import admin
from .models import Schedule, ScheduleExecution

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('name','project','cron','timezone','is_active','next_run_at')
    list_filter = ('is_active','timezone')

@admin.register(ScheduleExecution)
class ScheduleExecutionAdmin(admin.ModelAdmin):
    list_display = ('schedule','scheduled_for','status','created_at')
    list_filter = ('status',)
