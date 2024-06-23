from app.types import *
from app.services.PackageService import PackageService
from app.dao.PackageDao import PackageDao
from app.services.pipeline.YoloStage import run_yolo_stage
from app.services.pipeline.DescriptionStage import run_description_stage

async def begin_pipeline_processing(package: Package):
    """
    Create original_images
    """
    package = await preprocess_package(package)
    package = await run_yolo_stage(package)
    package = await run_description_stage(package)
    return package


async def preprocess_package(package: Package):
    package = await PackageService.create_original_images(package)
    return package
