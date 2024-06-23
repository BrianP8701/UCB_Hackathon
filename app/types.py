from pydantic import BaseModel
from typing import List, Dict
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
    pdfPath: str

class FeFormField(BaseModel):
    name: str
    description: str
    formFieldType: str

class FePackage(BaseModel):
    packageId: str
    packageName: str
    packageStatus: str
    originalPdfPath: str
    imagesWithBoxesPaths: List[str]
    formFields: List[FeFormField]
    filledOutPackages: List[FeFilledOutPackage]
    typeformUrl: str






"""
Backend types
"""

class PackageStatus(Enum):
    preprocessing = "Preprocessing"
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
    undetermined = "undetermined"

class FormField(BaseModel):
    id: str
    name: str
    description: str
    form_field_type: FormFieldType
    bounding_box: List[int]
    page: int

class FilledOutPackage(BaseModel):
    id: str
    email: str
    file_ids: List[str]

class Package(BaseModel):
    id: str
    name: str
    status: PackageStatus
    original_pdf_id: str
    original_image_ids: List[str] # In order of pages
    images_with_boxes_ids: List[str]
    form_fields: List[FormField]
    filled_out_packages: List[str]
    typeform_url: str

class File(BaseModel):
    id: str
    name: str
    content: bytes
