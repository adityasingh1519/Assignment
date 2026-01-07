# upload_service.py
import os
import tarfile
from django.core.files.uploadedfile import UploadedFile
from django.db import transaction

from api.models import Dataset, Event
from api.utils.ids import generate_dataset_id
from api.utils.event_parser import parse_event_line

def handle_event_upload(file_obj: UploadedFile) -> str:
    dataset_id = generate_dataset_id()
    
    try:
        with transaction.atomic():
            # Create dataset record
            dataset = Dataset.objects.create(
                dataset_id=dataset_id,
                file_name=file_obj.name
            )
            
            # Extract and parse tar.gz file
            events_to_create = []
            batch_size = 1000  # Batch insert for performance
            total_records = 0
            
            with tarfile.open(fileobj=file_obj, mode="r:gz") as tar:
                for member in tar.getmembers():
                    if member.isfile():
                        f = tar.extractfile(member)
                        if f:
                            for line in f:
                                line_str = line.decode('utf-8').strip()
                                event_data = parse_event_line(line_str)
                                
                                if event_data:
                                    events_to_create.append(Event(
                                        dataset=dataset,
                                        serialno=event_data['serialno'],
                                        version=event_data['version'],
                                        account_id=event_data['account_id'],
                                        instance_id=event_data['instance_id'],
                                        srcaddr=event_data['srcaddr'],
                                        dstaddr=event_data['dstaddr'],
                                        srcport=int(event_data['srcport']),
                                        dstport=int(event_data['dstport']),
                                        protocol=event_data['protocol'],
                                        packets=int(event_data['packets']),
                                        bytes=int(event_data['bytes']),
                                        starttime=int(event_data['starttime']),
                                        endtime=int(event_data['endtime']),
                                        action=event_data['action'],
                                        log_status=event_data['log_status'],
                                    ))
                                    
                                    total_records += 1
                                    
                                    # Batch insert every 1000 records
                                    if len(events_to_create) >= batch_size:
                                        Event.objects.bulk_create(events_to_create)
                                        events_to_create = []
            
            # Insert remaining events
            if events_to_create:
                Event.objects.bulk_create(events_to_create)
            
            # Update total records count
            dataset.total_records = total_records
            dataset.save()
            
        return dataset_id
        
    except Exception as e:
        # Transaction will auto-rollback on exception
        raise