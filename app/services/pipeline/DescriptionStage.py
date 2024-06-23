from app.types import *
from typing import Tuple
from app.dao.PackageDao import PackageDao
from app.services.PackageService import PackageService
import asyncio

from pydantic import Field
from app.dao.FileDao import FileDao

from app.services.InstructorService import InstructorService

instructor = InstructorService()

class ExtractFormFieldType(Enum):
    text = "text"
    date = "date"
    checkbox = "checkbox"
    signature = "signature"

class Description(BaseModel):
    name: str = Field(..., description="The name of the form field")
    description: str = Field(..., description="The description of the form field. The description needs to be very detailed encapuslating the full context of what goes in this field so we can dedupe later.")
    form_field_type: ExtractFormFieldType = Field(..., description="The type of the form field")

async def run_description_stage(package: Package):
    """
    Get all the images. Convert to base64 encoding.
    
    Asynchronously call instructorservice with each form field drawn on each image to extract name and description of 
    """
    package.status = PackageStatus.analyzing
    PackageDao.upsert(package)
    
    base64_images_with_boxes_and_form_fields: List[Tuple[str, FormField]] = await PackageService.get_image_with_boxes_for_each_form_field(package)
    FileDao.create_files_from_base64(base64_images=[image for image, _ in base64_images_with_boxes_and_form_fields], extension='.jpeg', identifier='description_boxes')
    
    # # Process in batches of 20
    # batch_size = 20
    # described_form_fields = []
    
    # for i in range(0, len(base64_images_with_boxes_and_form_fields), batch_size):
    #     batch = base64_images_with_boxes_and_form_fields[i:i + batch_size]
    #     tasks = [extract_description_from_image(image_base64, form_field) for image_base64, form_field in batch]
    #     results = await asyncio.gather(*tasks)
    #     described_form_fields.extend(results)
    
    # package.form_fields = described_form_fields
    # PackageDao.upsert(package)
    return package


async def extract_description_from_image(image_base64: str, form_field: FormField):
    """
    Extract the description from the image
    """
    description = await instructor.completion_with_base64_image_string(
        'You are helping to label the form field with the blue box drawn around it. You need to look at the image and using context, '
        'determine the name and description of the form field. You also need to determine the type of the form field, it can be '
        'text, date, checkbox, or signature.',
        image_base64,
        Description
    )

    form_field = FormField(
        id=form_field.id,
        name=description.name,
        description=description.description,
        form_field_type=FormFieldType(description.form_field_type.value),
        bounding_box=form_field.bounding_box,
        page=form_field.page
    )
    
    return form_field
