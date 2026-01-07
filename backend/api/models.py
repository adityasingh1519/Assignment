# models.py
from django.db import models

class Dataset(models.Model):
    dataset_id = models.CharField(max_length=32, unique=True, db_index=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    total_records = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.dataset_id} - {self.file_name}"

class Event(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='events')
    serialno = models.CharField(max_length=50)
    version = models.CharField(max_length=10)
    account_id = models.CharField(max_length=50, db_index=True)
    instance_id = models.CharField(max_length=50, db_index=True)
    srcaddr = models.GenericIPAddressField(db_index=True)  # Indexed
    dstaddr = models.GenericIPAddressField(db_index=True)  # Indexed
    srcport = models.IntegerField()
    dstport = models.IntegerField()
    protocol = models.CharField(max_length=10)
    packets = models.IntegerField()
    bytes = models.BigIntegerField()
    starttime = models.BigIntegerField(db_index=True)  # Indexed
    endtime = models.BigIntegerField(db_index=True)    # Indexed
    action = models.CharField(max_length=20, db_index=True)
    log_status = models.CharField(max_length=20)
    
    class Meta:
        indexes = [
            models.Index(fields=['srcaddr', 'starttime']),
            models.Index(fields=['dstaddr', 'starttime']),
            models.Index(fields=['starttime', 'endtime']),
            models.Index(fields=['dataset', 'starttime']),
        ]
        ordering = ['starttime']
    
    def __str__(self):
        return f"Event {self.id} - {self.srcaddr} -> {self.dstaddr}"