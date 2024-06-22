from app.utils.uuid import create_uuid
from typing import List
from app.database import Storage

storage = Storage()

class FileDao:
    @classmethod
    def create_files(file_bytes: List[bytes]) -> List[str]:
        file_ids = []
        for file in file_bytes:
            file_id = create_uuid()
            file_ids.append(file_id)
            storage.create(file_id, file)
        return file_ids

    @classmethod
    def get_file(file_id: str) -> bytes:
        return storage.read(file_id)
