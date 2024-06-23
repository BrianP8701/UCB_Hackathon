from app.types import *
from app.utils import get_path_from_file_id
from app.services.YoloService import YoloService
from app.utils import create_uuid
from app.dao.PackageDao import PackageDao
from app.services.PackageService import PackageService

import logging

async def run_yolo_stage(package: Package):
    """
    Convert all files to images.
    
    Create all form fields.
    """
    package.status = PackageStatus.detecting
    PackageDao.upsert(package)

    image_ids = package.original_image_ids
    image_paths = [get_path_from_file_id(image_id) for image_id in image_ids]
    yolo_service = YoloService()


    form_fields: List[FormField] = []
    for i, image_path in enumerate(image_paths):
        detected_boxes: List[List[str]] = yolo_service.predict(image_path)
        logging.info(f'detected_boxes: {detected_boxes}')
        for box in detected_boxes:
            form_field = FormField(
                    id=create_uuid('form_field'),
                    name="",
                    description="",
                    form_field_type=FormFieldType.undetermined,
                    bounding_box=box,
                    page=i
                )
            form_fields.append(form_field)

    logging.info(f'form_fields: {form_fields}')
    package.form_fields = form_fields
    PackageDao.upsert(package)

    await PackageService.create_images_with_boxes(package)
    
    return package
