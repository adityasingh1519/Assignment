
from django.db.models import Q
from api.models import Event

PAGE_SIZE = 10

def search_dataset(
    dataset_id,
    query,
    start_time,
    end_time,
    page=1,
    limit=PAGE_SIZE,
):
    queryset = Event.objects.filter(dataset__dataset_id=dataset_id)
    
    if start_time is not None:
        queryset = queryset.filter(starttime__gte=start_time)
    
    if end_time is not None:
        queryset = queryset.filter(endtime__lte=end_time)
    
    if query:
        q = query.lower()
        queryset = queryset.filter(
            Q(account_id__icontains=q) |
            Q(instance_id__icontains=q) |
            Q(srcaddr__icontains=q) |
            Q(dstaddr__icontains=q) |
            Q(action__icontains=q) |
            Q(log_status__icontains=q)
        )
    
    total_count = queryset.count()
    
    offset = (page - 1) * limit
    results = queryset[offset:offset + limit]
    
    events = []
    for event in results:
        events.append({
            'source_file_name': event.source_file_name,
            'srcaddr': event.srcaddr,
            'dstaddr': event.dstaddr,
            'action': event.action,
            'log_status': event.log_status,
        })
    
    has_more = (offset + limit) < total_count
    
    return events, total_count, has_more