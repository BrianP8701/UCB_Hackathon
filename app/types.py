from pydantic import BaseModel
from typing import List

class File(BaseModel):
    name: str
    content: bytes

class PackageRow(BaseModel):
    packageId: str
    packageName: str
    packageStatus: str

class Package(BaseModel):
    packageId: str
    packageName: str
    packageStatus: str
    rawFiles: List[File]
    labeledFiles: List[File]

class PackageFormRow(BaseModel):
    packageFormId: str
    packageName: str
    name: str

class PackageForm(BaseModel):
    packageFormId: str
    packageName: str
    name: str
    typeformUrl: str
    files: List[File]