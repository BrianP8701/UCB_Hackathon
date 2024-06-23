from typing import List
from app.utils import create_uuid
import cv2
import numpy as np
import logging

from app.dao.FileDao import FileDao
from app.types import PackageStatus, Package
from app.dao.PackageDao import PackageDao
from app.services.PdfService import PdfService
from app.database import Storage
from app.utils import get_path_from_file_id, create_uuid

class PackageService:
    @classmethod
    async def create_package(cls, name: str, file_bytes: List[bytes]) -> Package:
        """
        Merges all files into one pdf and saves it. Creates pdf object with 
        """
        file = PdfService.merge_pdfs(file_bytes)
        file_ids = FileDao.create_files([file], '.pdf', 'original_pdf')

        package = Package(
            id=create_uuid('package'),
            name=name,
            status=PackageStatus.preprocessing,
            original_pdf_id=file_ids[0],
            original_image_ids=[],
            images_with_boxes_ids=[],
            form_fields=[],
            filled_out_packages=[],
            typeform_url=""
        )

        PackageDao.upsert(package)
        return package


    @classmethod
    async def create_original_images(cls, package: Package) -> Package:
        """
        Creates images from pdf and saves them to storage
        """
        images = PdfService.convert_pdf_to_images(package.original_pdf_id)
        image_ids = FileDao.create_files(images, '.jpeg', 'original_image')
        package.original_image_ids = image_ids
        PackageDao.upsert(package)
        return package

    @classmethod
    async def draw_bounding_boxes_on_image(cls, image: np.ndarray, bounding_boxes: List[List[int]]) -> np.ndarray:
        for bounding_box in bounding_boxes:
            if len(bounding_box) == 4:
                cv2.rectangle(image, (bounding_box[0], bounding_box[1]), (bounding_box[2], bounding_box[3]), (255, 0, 0), 3)
        return image

    @classmethod
    async def create_images_with_boxes(cls, package: Package) -> Package:
        storage = Storage()
        original_image_ids = package.original_image_ids
        original_image_paths = [get_path_from_file_id(image_id) for image_id in original_image_ids]

        images = [cv2.imread(image_path) for image_path in original_image_paths]

        for field_form in package.form_fields:
            images[field_form.page] = await cls.draw_bounding_boxes_on_image(images[field_form.page], [field_form.bounding_box])

        imagesWithBoxesIds = FileDao.create_files(images, '.jpeg', 'image_with_boxes')
        image_bytes = [cv2.imencode('.jpeg', image)[1] for image in images]
        image_ids = storage.batch_create(imagesWithBoxesIds, image_bytes)
        package.images_with_boxes_ids = image_ids
        PackageDao.upsert(package)
        return package
