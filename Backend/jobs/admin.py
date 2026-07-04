from django.contrib import admin
from .models import Job, JobExecution, DeadLetter, ScheduledJob

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id','queue','type','status','attempts','created_at')
    list_filter = ('status','type')
    search_fields = ('id','payload')

@admin.register(JobExecution)
class JobExecutionAdmin(admin.ModelAdmin):
    list_display = ('job','worker','status','started_at','finished_at')

@admin.register(DeadLetter)
class DeadLetterAdmin(admin.ModelAdmin):
    list_display = ('job','moved_at')

@admin.register(ScheduledJob)
class ScheduledJobAdmin(admin.ModelAdmin):
    list_display = ('name','project','cron','is_active')
