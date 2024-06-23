import logging

from app.types import *
from app.dao.PackageDao import PackageDao

from pydantic import Field

from app.services.TypeformService import TypeformService


typeformService = TypeformService()

async def run_create_stage(package: Package):
    """
    Create a typeform form and return the form id and url
    """
    package.status = PackageStatus.create
    PackageDao.upsert(package)

    typeform_schema = typeformService.build_typeform_schema(package.final_form)
    response, form_id, form_url = typeformService.create_form(typeform_schema)
    package.typeform_id = form_id
    package.typeform_url = form_url
    logging.info(f'Typeform form created: {package}')
    logging.info(f'Typeform form id: {form_id}')
    logging.info(f'Typeform form url: {form_url}')
    PackageDao.upsert(package)

    return package
