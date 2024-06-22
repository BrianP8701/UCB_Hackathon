from pydantic import BaseModel
from typing import List


"""
Frontend types
"""
enum

class File(BaseModel):
    name: str
    content: bytes

class PackageRow(BaseModel):
    packageId: str
    packageName: str
    packageStatus: str

class FilledOutPackage(BaseModel):
    email: str
    pdfs: List[str]

class Package(BaseModel):
    packageId: str
    packageName: str
    packageStatus: str
    originalPdfs: List[str]
    imagesWithBoxes: List[str]
    formFields: List[FormField]
    filledOutPackages: List[FilledOutPackage]
    googleFormUrl: str



class FormField(BaseModel):
    name: str
    description: str
    form_field_type: FormFieldType