from fastapi import FastAPI

from app.types import *
from app.dao.PackageDao import PackageDao

app = FastAPI()

@app.post("/createPackage")
async def create_package(files: List[File], name: str) -> List[PackageRow]:
    packageDao = PackageDao()
    package = packageDao.create_package(name, files)
    return {"packageRows": [{"packageId": package.id, "packageName": package.name, "packageStatus": package.status}]}

@app.get("/getPackagesRows")
async def get_packages_rows() -> List[PackageRow]:
    return {"packageRows": [{"packageId": "123", "packageName": "Sample Package", "packageStatus": "complete"}]}

@app.get("/getPackage")
async def get_package(packageId: str) -> Package:
    return {"package": {"packageId": packageId, "packageName": "Sample Package", "packageStatus": "complete", "rawFiles": [], "labeledFiles": []}}
