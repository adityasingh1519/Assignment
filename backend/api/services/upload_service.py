
import os
import tarfile
from typing import Iterator, List
from django.core.files.uploadedfile import UploadedFile
from django.db import transaction, connection

from api.models import Dataset, Event
from api.utils.ids import generate_dataset_id
from api.utils.event_parser import parse_event_line


def batch_iterator(iterator: Iterator, batch_size: int):
    batch = []
    for item in iterator:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def create_events_generator(tar: tarfile.TarFile, dataset_id: int):
    for member in tar.getmembers():
        if not member.isfile():
            continue

        source_file_name = os.path.basename(member.name)
        extracted_file = tar.extractfile(member)
        
        if not extracted_file:
            continue

        for line in extracted_file:
            line_str = line.decode("utf-8", errors="ignore").strip()
            event_data = parse_event_line(line_str)

            if not event_data:
                continue

            yield Event(
                dataset_id=dataset_id,
                source_file_name=source_file_name,
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
            )


def handle_event_upload(file_obj: UploadedFile) -> str:
    dataset_id = generate_dataset_id()
    batch_size = 50000 
    total_records = 0

    try:
        dataset = Dataset.objects.create(
            dataset_id=dataset_id,
            file_name=file_obj.name
        )

        with tarfile.open(fileobj=file_obj, mode="r:gz") as tar:
            event_generator = create_events_generator(tar, dataset.id)
            
            for batch in batch_iterator(event_generator, batch_size):
                Event.objects.bulk_create(
                    batch,
                    batch_size=batch_size,
                    ignore_conflicts=False
                )
                total_records += len(batch)

        dataset.total_records = total_records
        dataset.save(update_fields=['total_records'])

        return dataset_id

    except Exception:
        Dataset.objects.filter(dataset_id=dataset_id).delete()
        raise