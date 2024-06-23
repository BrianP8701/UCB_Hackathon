from app.types import *
from typing import Optional, Tuple
from app.dao.PackageDao import PackageDao
import logging

from app.utils import create_uuid

from pydantic import Field

from app.services.InstructorService import InstructorService


instructor = InstructorService()


class MapFormField(BaseModel):
    no_mapping: bool = Field(..., description="Whether or not the field we are looking at has maps to a field in the existing form. If none of the existing fields map to this field, output True. Otherwise if there is a mapping, output False.")
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
    for i in range(len(form_fields)):
        final_form, form_fields = await update_mapping(i, form_fields, final_form)
    
    package.final_form = final_form
    package.form_fields = form_fields

    PackageDao.upsert(package)

    return package


async def update_mapping(current_index: int, existing_form_fields: List[FormField], final_form: List[FormField]) -> Tuple[List[FormField], List[FormField]]:
    current_form_field = existing_form_fields[current_index]
    current_form_field_type = current_form_field.form_field_type
    form_fields_with_same_type = get_form_fields_with_same_type(final_form, current_form_field_type)
    final_form_string = stringify_existing_form(form_fields_with_same_type)
    
    mapping = await instructor.completion(
        prompt=f"{final_form_string}\n\nCurrent form field to map: {current_form_field.name}\nDescription: {current_form_field.description}",
        instructor_model=MapFormField
    )
    
    if not mapping.no_mapping:
        new_final_form_field = FormField(
            id=create_uuid('final_form_field'),
            name=current_form_field.name,
            description=current_form_field.description,
            form_field_type=current_form_field.form_field_type,
            bounding_box=[],
            page=-1,
            mapping=[current_index]
        )
        final_form.append(new_final_form_field)
        existing_form_fields[current_index].mapping.append(mapping.index)
    else:
        final_form[mapping.index].mapping.append(current_index)
        existing_form_fields[current_index].mapping.append(mapping.index)

    return final_form, existing_form_fields


def get_form_fields_with_same_type(form_fields: List[FormField], form_field_type: FormFieldType) -> List[FormField]:
    return [form_field for form_field in form_fields if form_field.form_field_type == form_field_type]


def stringify_existing_form(existing_form: List[FormField]) -> str:
    return "\n\n".join(
        f"{i}. {field.name}\nDescription: {field.description}"
        for i, field in enumerate(existing_form)
    )
