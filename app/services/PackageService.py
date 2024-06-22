from typing import List
from app.utils.uuid import create_uuid

from app.dao.FileDao import FileDao
from app.types import PackageStatus, Package
from app.dao.PackageDao import PackageDao

class PackageService:
    @classmethod
    def create_package(name: str, file_bytes: List[bytes]) -> None:
        file_ids = FileDao.create_files(file_bytes)
        package = Package(
            id=create_uuid(),
            name=name,
            status=PackageStatus.detecting,
            original_pdf_paths=file_ids,
            images_with_boxes_paths=[],
            form_fields=[],
            filled_out_packages=[],
            google_form_url=""
        )
        PackageDao.create_package(package)
        return package
