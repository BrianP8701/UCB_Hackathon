from typing import List
from app.utils.uuid import create_uuid

from app.dao.FileDao import FileDao
from app.types import PackageStatus, Package
from app.dao.PackageDao import PackageDao
from app.services.PdfService import PdfService

class PackageService:
    @classmethod
    async def create_package(cls, name: str, file_bytes: List[bytes]) -> Package:
        """
        Returns package with just original pdf id
        """
        file = PdfService.merge_pdfs(file_bytes)
        file_ids = FileDao.create_files([file])

        package = Package(
            id=create_uuid(),
            name=name,
            status=PackageStatus.detecting,
            original_pdf_id=file_ids[0],
            original_image_ids=[],
            images_with_boxes_ids=[],
            form_fields=[],
            filled_out_package_ids=[],
            google_form_url=""
        )

        PackageDao.create_package(package)
        return package
