import logging

from app.types import *
from app.services.PackageService import PackageService
from app.dao.PackageDao import PackageDao
from app.services.pipeline.YoloStage import run_yolo_stage
from app.services.pipeline.DescriptionStage import run_description_stage
from app.services.pipeline.DedupeStage import run_dedupe_stage
from app.services.pipeline.CreateStage import run_create_stage

async def begin_pipeline_processing(package: Package):
    """
    Create original_images
    """
    package = await preprocess_package(package)
    logging.info(f'Preprocessed package: {package}')
    package = await run_yolo_stage(package)
    logging.info(f'Yolo stage complete: {package}')
    package = await run_description_stage(package)
    logging.info(f'Description stage complete: {package}')
    package = await run_dedupe_stage(package)
    logging.info(f'Dedupe stage complete: {package}')
    package = await run_create_stage(package)
    logging.info(f'Create stage complete: {package}')

    package.status = PackageStatus.complete
    PackageDao.upsert(package)

    return package


async def preprocess_package(package: Package):
    package = await PackageService.create_original_images(package)
    return package
