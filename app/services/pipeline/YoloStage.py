from app.types import *
from app.utils import get_path_from_file_id
from app.services.YoloService import YoloService
from app.utils import create_uuid
from app.dao.PackageDao import PackageDao
from app.services.PackageService import PackageService
from app.services.PdfService import PdfService

async def run_yolo_stage(package: Package):
    """
    Convert all files to images.
    
    Create all form fields.
    """
    package.status = PackageStatus.detecting
    PackageDao.upsert(package)
    form_fields: List[FormField] = []
    
    original_pdf_path = get_path_from_file_id(package.original_pdf_id)
    total_count, widget_form_fields = PdfService.get_form_fields_and_rectangles(original_pdf_path)
    
    if total_count > 0:
        for i, form_field_page in enumerate(widget_form_fields):
            for form_field in form_field_page:
                form_field = FormField(
                    id=create_uuid('form_field'),
                    name="",
                    description="",
                    form_field_type=form_field[1],
                    bounding_box=form_field[0],
                    page=i
                )
                form_fields.append(form_field)
        package.form_fields = form_fields
        PackageDao.upsert(package)
        await PackageService.create_images_with_boxes(package)
        return package

    image_ids = package.original_image_ids
    image_paths = [get_path_from_file_id(image_id) for image_id in image_ids]
    yolo_service = YoloService()


    
    for i, image_path in enumerate(image_paths):
        detected_boxes: List[List[str]] = yolo_service.predict(image_path)
        for box in detected_boxes:
            if box:
                form_field = FormField(
                        id=create_uuid('form_field'),
                        name="",
                        description="",
                        form_field_type=FormFieldType.undetermined,
                        bounding_box=box,
                        page=i
                    )
                form_fields.append(form_field)

    package.form_fields = form_fields
    PackageDao.upsert(package)

    await PackageService.create_images_with_boxes(package)
    
    return package
