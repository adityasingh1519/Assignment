

import os
import tarfile
import shutil
from django.core.files.uploadedfile import UploadedFile

from api.utils.ids import generate_dataset_id
from api.utils.file_utils import get_dataset_dir


def handle_event_upload(file_obj: UploadedFile) -> str:
    
    dataset_id = generate_dataset_id()
    dataset_dir = get_dataset_dir(dataset_id)
    
    os.makedirs(dataset_dir, exist_ok=True)
    
    try:
        with tarfile.open(fileobj=file_obj, mode='r:gz') as tar:
            tar.extractall(path=dataset_dir)
        return dataset_id
    except Exception as e:
        if(os.path.exists(dataset_dir)):
            shutil.remove(dataset_dir)
        raise
