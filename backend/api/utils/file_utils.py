import os
from django.conf import settings

def get_dataset_dir(dataset_id: str) -> str:
    return os.path.join(settings.EVENT_FILES_DIR, "datasets", dataset_id)


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)
