from app.utils import create_uuid
from typing import List
from app.database import Storage

storage = Storage()

class FileDao:
    @classmethod
    def create_files(cls, file_bytes: List[bytes], extension: str, identifier: str) -> List[str]:
        file_ids = []
        for file in file_bytes:
            file_id = create_uuid(identifier) + extension
            file_ids.append(file_id)
            storage.create(file_id, file)
        return file_ids

    @classmethod
    def get_file(cls, file_id: str) -> bytes:
        bytes = storage.read(file_id)
        if bytes is None:
            raise ValueError(f"File with id {file_id} not found")
        return bytes
