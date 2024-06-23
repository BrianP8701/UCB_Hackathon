import uuid
from dotenv import load_dotenv
import os

load_dotenv()

def create_uuid() -> str:
    return str(uuid.uuid4())

def get_path_from_file_id(file_id: str) -> str:
    storage_path = os.getenv("STORAGE_PATH")
    return os.path.join(storage_path, file_id)
