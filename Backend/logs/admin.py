from django.contrib import admin
from .models import LogEntry

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('timestamp','level','event_type','message')
    list_filter = ('level','event_type')
    search_fields = ('message','meta')
    readonly_fields = ('timestamp','level','event_type','message')
