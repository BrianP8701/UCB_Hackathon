from app.utils import create_uuid
from typing import List
from app.database import Storage
import base64

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
    def create_files_from_base64(cls, base64_images: List[str], extension: str, identifier: str) -> List[str]:
        file_ids = []
        for base64_image in base64_images:
            file_bytes = base64.b64decode(base64_image)
            file_id = create_uuid(identifier) + extension
            file_ids.append(file_id)
            storage.create(file_id, file_bytes)
        return file_ids

    @classmethod
    def get_file(cls, file_id: str) -> bytes:
        bytes = storage.read(file_id)
        if bytes is None:
            raise ValueError(f"File with id {file_id} not found")
        return bytes
