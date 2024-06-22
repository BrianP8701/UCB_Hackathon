from fastapi import FastAPI
from app.types import *

app = FastAPI()

@app.post("/processPackage")
async def process_package(files: List[File], name: str):
    return {"packageRows": [{"packageId": "123", "packageName": name, "packageStatus": "complete"}]}

@app.get("/getPackagesRows")
async def get_packages_rows():
    return {"packageRows": [{"packageId": "123", "packageName": "Sample Package", "packageStatus": "complete"}]}

@app.get("/getPackage")
async def get_package(packageId: str):
    return {"package": {"packageId": packageId, "packageName": "Sample Package", "packageStatus": "complete", "rawFiles": [], "labeledFiles": []}}

@app.post("/createPackageForm")
async def create_package_form(name: str, packageId: str):
    return {"packageFormRows": [{"packageFormId": "form123", "packageName": "Form Package", "name": name}]}

@app.get("/getPackageForm")
async def get_package_form(packageFormId: str):
    return {"packageForm": {"packageFormId": packageFormId, "packageName": "Form Package", "name": "Sample Form", "typeformUrl": "http://example.com", "files": []}}

@app.get("/getPackageFormRows")
async def get_package_form_rows():
    return {"packageFormRows": [{"packageFormId": "form123", "packageName": "Form Package", "name": "Sample Form"}]}
