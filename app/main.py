from fastapi import FastAPI

from app.types import *
from app.dao.PackageDao import PackageDao

app = FastAPI()

@app.post("/processPackage")
async def process_package(files: List[File], name: str) -> List[PackageRow]:
    packageDao = PackageDao()
    package = packageDao.create_package(name, files)
    return {"packageRows": [{"packageId": package.id, "packageName": package.name, "packageStatus": package.status}]}

@app.get("/getPackagesRows")
async def get_packages_rows() -> List[PackageRow]:
    return {"packageRows": [{"packageId": "123", "packageName": "Sample Package", "packageStatus": "complete"}]}

@app.get("/getPackage")
async def get_package(packageId: str) -> Package:
    return {"package": {"packageId": packageId, "packageName": "Sample Package", "packageStatus": "complete", "rawFiles": [], "labeledFiles": []}}

@app.post("/createPackageForm")
async def create_package_form(name: str, packageId: str) -> List[PackageFormRow]:
    return {"packageFormRows": [{"packageFormId": "form123", "packageName": "Form Package", "name": name}]}

@app.get("/getPackageForm")
async def get_package_form(packageFormId: str) -> PackageForm:
    return {"packageForm": {"packageFormId": packageFormId, "packageName": "Form Package", "name": "Sample Form", "typeformUrl": "http://example.com", "files": []}}

@app.get("/getPackageFormRows")
async def get_package_form_rows() -> List[PackageFormRow]:
    return {"packageFormRows": [{"packageFormId": "form123", "packageName": "Form Package", "name": "Sample Form"}]}
