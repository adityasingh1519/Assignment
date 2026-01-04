

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
        with tarfile.open(fileobj=file_obj, mode="r:gz") as tar:
                members = tar.getmembers()

                # detect top-level directory
                root_dirs = {
                    member.name.split("/")[0]
                    for member in members
                    if member.name and "/" in member.name
                }

                strip_root = len(root_dirs) == 1
                root_dir = next(iter(root_dirs)) if strip_root else None

                for member in members:
                    if strip_root:
                        member.name = member.name.replace(f"{root_dir}/", "", 1)
                    if member.name:  # avoid empty root
                        tar.extract(member, path=dataset_dir)

        return dataset_id
    except Exception as e:
        if(os.path.exists(dataset_dir)):
            shutil.remove(dataset_dir)
        raise
