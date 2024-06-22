import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Storage:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Storage, cls).__new__(cls)
            cls._instance.storage_path = os.getenv('STORAGE_PATH')
        return cls._instance

    def create(self, file_path: str, file_bytes: bytes, extension: str) -> None:
        full_path = os.path.join(self.storage_path, file_path, extension)
        with open(full_path, 'wb') as file:
            file.write(file_bytes)

    def read(self, file_path: str) -> Optional[bytes]:
        full_path = os.path.join(self.storage_path, file_path)
        if not os.path.exists(full_path):
            return None
        with open(full_path, 'rb') as file:
            return file.read()
