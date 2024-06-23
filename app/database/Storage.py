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

    def create(self, file_path: str, file_bytes: bytes) -> None:
        full_path = os.path.join(self.storage_path, file_path)
        with open(full_path, 'wb') as file:
            file.write(file_bytes)

    def batch_create(self, file_paths: list, file_bytes: list) -> list:
        created_files = []
        for file_path, file_bytes in zip(file_paths, file_bytes):
            self.create(file_path, file_bytes)
            created_files.append(file_path)
        return created_files

    def read(self, file_path: str) -> Optional[bytes]:
        full_path = os.path.join(self.storage_path, file_path)
        if not os.path.exists(full_path):
            return None
        with open(full_path, 'rb') as file:
            return file.read()
