import uuid

def generate_dataset_id() -> str:
    return uuid.uuid4().hex
