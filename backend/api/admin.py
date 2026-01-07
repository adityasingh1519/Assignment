# admin.py
from django.contrib import admin
from .models import Dataset, Event

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['dataset_id', 'file_name', 'total_records', 'uploaded_at']
    search_fields = ['dataset_id', 'file_name']
    readonly_fields = ['dataset_id', 'uploaded_at']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'dataset', 'srcaddr', 'dstaddr', 'starttime', 'endtime', 'action']
    list_filter = ['action', 'log_status', 'dataset']
    search_fields = ['srcaddr', 'dstaddr', 'account_id', 'instance_id']
    raw_id_fields = ['dataset']
    list_per_page = 50