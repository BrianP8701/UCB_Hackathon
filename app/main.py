from fastapi import FastAPI, BackgroundTasks

from app.types import *
from app.dao.PackageDao import PackageDao
from app.pipeline import begin_pipeline_processing
from app.formatters import *

app = FastAPI()


class CreatePackageRequest(BaseModel):
    files: List[bytes]
    name: str

@app.post("/createPackage")
async def create_package(request: CreatePackageRequest, background_tasks: BackgroundTasks) -> FePackage:
    packageDao = PackageDao()
    package: Package = packageDao.create_package(request.name, request.files)

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
    return package_to_fe_package(package)


class GetPackageStatusRequest(BaseModel):
    id: str

@app.get("/getPackageStatus")
async def get_package_status(request: GetPackageStatusRequest) -> str:
    package: Package = PackageDao.get_package(request.id)
    return package.status.value
