from pydantic import BaseModel
from typing import List
from enum import Enum


"""
Frontend types
"""
class FePackageRow(BaseModel):
    packageId: str
    packageName: str
    packageStatus: str

class FeFilledOutPackage(BaseModel):
    email: str
    pdfPaths: List[str]

class FeFormField(BaseModel):
    name: str
    description: str
    formFieldType: str

class FePackage(BaseModel):
    packageId: str
    packageName: str
    packageStatus: str
    originalPdfPaths: List[str]
    imagesWithBoxesPaths: List[str]
    formFields: List[FeFormField]
    filledOutPackages: List[FeFilledOutPackage]
    googleFormUrl: str







"""
Backend types
"""

class PackageStatus(Enum):
    detecting = "Detecting Form Boxes with YOLO"
    analyzing = "Analyzing Form Boxes With GPT4o"
    creating = "Creating Form with GPT4o"
    complete = "Complete"

class FormFieldType(Enum):
    text = "text"
    number = "number"
    date = "date"
    checkbox = "checkbox"
    dropdown = "dropdown"

class File(BaseModel):
    id: str
    name: str
    content: bytes

class FormField(BaseModel):
    name: str
    description: str
    form_field_type: FormFieldType

class FilledOutPackage(BaseModel):
    email: str
    file_ids: List[str]

class Package(BaseModel):
    id: str
    name: str
    status: PackageStatus
    original_pdf_paths: List[str]
    images_with_boxes_paths: List[str]
    form_fields: List[FormField]
    filled_out_packages: List[FilledOutPackage]
    google_form_url: str



class File(BaseModel):
    id: str
    name: str
    content: bytes


