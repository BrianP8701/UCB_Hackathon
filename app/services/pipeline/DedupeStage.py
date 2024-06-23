from app.types import *
from typing import Optional
from app.dao.PackageDao import PackageDao

from pydantic import Field

from app.services.InstructorService import InstructorService


instructor = InstructorService()


class MapFormField(BaseModel):
    no_mapping: bool = Field(..., description="Whether or not the field we are looking at has maps to a field in the existing form. If not output false, and we'll add this field as a new field in the form.")
    index: int = Field(..., description="If the field has a mapping, output the index of the field to map to. Otherwise, output -1 ")


async def run_dedupe_stage(package: Package):
    """
    Final form should be a list of field forms.
    Map all extracted_form_fields to fields in the final form.
    """
    package.status = PackageStatus.dedupe
    PackageDao.upsert(package)

    form_fields = package.form_fields
    final_form = []
    for form_field in form_fields:
        map_form_field
    
    return package


async def update_mapping(current_index: int, existing_form_fields: List[FormField], final_form: List[FormField]) -> List[FormField]:
    current_form_field_to_map = existing_form_fields[current_index]
    current_form_field_type = current_form_field_to_map.type
    form_fields_with_same_type = get_form_fields_with_same_type(final_form, current_form_field_type)
    final_form_string = stringify_existing_form(form_fields_with_same_type)
    
    mapping = await instructor.completion(
        prompt=f"{final_form_string}\n\nCurrent form field to map: {current_form_field_to_map.name}\nDescription: {current_form_field_to_map.description}",
        instructor_model=MapFormField
    )
    
    if mapping.no_mapping:
        return MapFormField(no_mapping=True, index=-1)
    
    return MapFormField(no_mapping=False, index=mapping.index)


def get_form_fields_with_same_type(form_fields: List[FormField], form_field_type: FormFieldType) -> List[FormField]:
    return [form_field for form_field in form_fields if form_field.type == form_field_type]


def stringify_existing_form(existing_form: List[FormField]) -> str:
    return "\n\n".join(
        f"{i+1}. {field.name}\nDescription: {field.description}"
        for i, field in enumerate(existing_form)
    )