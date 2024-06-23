from typing import List, Tuple
from app.utils import create_uuid
import cv2
import numpy as np
import base64
import logging

from app.dao.FileDao import FileDao
from app.types import PackageStatus, Package, FormField, TypeformResponse, FilledOutPackage
from app.dao.PackageDao import PackageDao
from app.services.PdfService import PdfService
from app.database import Storage
from app.utils import get_path_from_file_id, create_uuid
from app.services.TypeformService import TypeformService
from app.formatters import package_to_fe_package

typeformService = TypeformService()

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
            final_form=[],
            typeform_json_schema={},
            filled_out_packages=[],
            typeform_url="",
            typeform_id=''
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

    @classmethod
    async def get_image_with_boxes_for_each_form_field(cls, package: Package) -> List[Tuple[str, FormField]]:
        """
        Get the image with box as base64 string for each form field
        """
        original_image_ids = package.original_image_ids
        original_image_paths = [get_path_from_file_id(image_id) for image_id in original_image_ids]

        images = [cv2.imread(image_path) for image_path in original_image_paths]
        
        form_fields = package.form_fields
        
        result = []

        for form_field in form_fields:
            page = form_field.page
            bounding_box = form_field.bounding_box
            image_with_box = images[page]
            image_with_box = await cls.draw_bounding_boxes_on_image(image_with_box, [bounding_box])
            _, buffer = cv2.imencode('.jpeg', image_with_box)
            image_base64 = base64.b64encode(buffer).decode('utf-8')
            result.append((image_base64, form_field))

        return result

    @classmethod
    async def get_package(cls, package_id: str) -> Package:
        package = PackageDao.get_package(package_id)
        package = await cls.update_filled_out_packages(package)
        
        
        return package

    @classmethod
    async def update_filled_out_packages(cls, package: Package) -> Package:
        existing_filled_out_packages = package.filled_out_packages
        existing_filled_out_package_ids = [filled_out_package.id for filled_out_package in existing_filled_out_packages]
        all_typeform_responses: List[TypeformResponse] = typeformService.get_all_responses(package.typeform_id)
        logging.info(f'All typeform responses: {all_typeform_responses}')
        
        print()
        for typeform_response in all_typeform_responses:
            if typeform_response.id not in existing_filled_out_package_ids:
                logging.info(f'Creating filled out package for typeform response: {typeform_response.id}')
                filled_out_package: FilledOutPackage = PdfService.create_filled_out_package(package, typeform_response)
                existing_filled_out_packages.append(filled_out_package)
        print()
        
        package.filled_out_packages = existing_filled_out_packages
        PackageDao.upsert(package)
        return package
