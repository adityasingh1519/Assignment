# search_service.py
from django.db.models import Q
from api.models import Event

PAGE_SIZE = 50

def search_dataset(
    dataset_id,
    query,
    start_time,
    end_time,
    page=1,
    limit=PAGE_SIZE,
):
    # Base query
    queryset = Event.objects.filter(dataset__dataset_id=dataset_id)
    
    # Apply time range filters (using indexed fields)
    if start_time is not None:
        queryset = queryset.filter(starttime__gte=start_time)
    
    if end_time is not None:
        queryset = queryset.filter(endtime__lte=end_time)
    
    # Apply text search across multiple fields
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
    
    # Get total count before pagination
    total_count = queryset.count()
    
    # Apply pagination
    offset = (page - 1) * limit
    results = queryset[offset:offset + limit]
    
    # Convert to list of dicts
    events = []
    for event in results:
        events.append({
            'id': event.id,
            'serialno': event.serialno,
            'version': event.version,
            'account_id': event.account_id,
            'instance_id': event.instance_id,
            'srcaddr': event.srcaddr,
            'dstaddr': event.dstaddr,
            'srcport': event.srcport,
            'dstport': event.dstport,
            'protocol': event.protocol,
            'packets': event.packets,
            'bytes': event.bytes,
            'starttime': event.starttime,
            'endtime': event.endtime,
            'action': event.action,
            'log_status': event.log_status,
        })
    
    has_more = (offset + limit) < total_count
    
    return events, total_count, has_more