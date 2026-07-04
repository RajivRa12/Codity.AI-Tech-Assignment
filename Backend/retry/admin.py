from django.contrib import admin
from .models import RetryPolicy, RetryAttempt

@admin.register(RetryPolicy)
class RetryPolicyAdmin(admin.ModelAdmin):
    list_display = ('name','policy_type','initial_delay_seconds','backoff_factor','max_retries')
    search_fields = ('name',)

@admin.register(RetryAttempt)
class RetryAttemptAdmin(admin.ModelAdmin):
    list_display = ('job','attempt_number','status','scheduled_for','executed_at')
    list_filter = ('status',)
