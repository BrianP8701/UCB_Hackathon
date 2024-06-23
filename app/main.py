from fastapi import FastAPI, BackgroundTasks
import base64
import logging

from app.types import *
from app.dao.PackageDao import PackageDao
from app.pipeline import begin_pipeline_processing
from app.formatters import *
from app.services.PackageService import PackageService

app = FastAPI()

logging.basicConfig(
    filename='app.log',  # Log file name
    level=logging.INFO,  # Log level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date format
)

class CustomFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.stream.write('\n\n')  # Add two new lines
        self.flush()

# Replace the default handler with the custom handler
for handler in logging.getLogger().handlers:
    if isinstance(handler, logging.FileHandler):
        logging.getLogger().removeHandler(handler)

logging.getLogger().addHandler(CustomFileHandler('app.log'))


class CreatePackageRequest(BaseModel):
    files: List[bytes]
    name: str

@app.post("/createPackage")
async def create_package(request: CreatePackageRequest, background_tasks: BackgroundTasks) -> FePackage:
    decoded_files = [base64.b64decode(file) for file in request.files]  # Decode base64 strings to bytes
    package: Package = await PackageService.create_package(request.name, decoded_files)

    background_tasks.add_task(begin_pipeline_processing, package)

    return package_to_fe_package(package)

@app.get("/getPackagesRows")
async def get_packages_rows() -> List[FePackageRow]:
    return PackageDao.get_package_rows()



class GetPackageRequest(BaseModel):
    id: str

@app.get("/getPackage")
async def get_package(packageId: str) -> FePackage:
    package: Package = PackageDao.get_package(packageId)
    logging.info(f'package: {package}')
    return package_to_fe_package(package)

@app.get("/getPackageStatus")
async def get_package_status(packageId: str) -> str:
    package: Package = PackageDao.get_package(packageId)
    logging.info(f'package: {package}')
    logging.info(f'package.status: {package.status}')
    logging.info(f'package.status.value: {package.status.value}')
    return package.status.value
