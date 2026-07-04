from django.contrib import admin
from .models import Queue

@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('name','project','priority','concurrency_limit','is_paused','created_at')
    list_filter = ('is_paused','priority')
    search_fields = ('name','project__name')
