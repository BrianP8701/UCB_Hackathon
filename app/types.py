from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from enum import Enum


"""
Frontend types
"""
class FePackageRow(BaseModel):
    packageId: str
    packageName: str
    packageStatus: str

class FeFilledOutPackage(BaseModel):
    pdfPath: str
    email: str

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
    filledOutPackages: List[FeFilledOutPackage]
    typeformUrl: str
    typeformId: str






"""
Backend types
"""

class PackageStatus(Enum):
    preprocessing = "Preprocessing"
    detecting = "Detecting Form Boxes with YOLO"
    analyzing = "Analyzing Form Boxes With GPT4o"
    dedupe = "Deduplicating Form Fields"
    create = "Creating Typeform Form"
    complete = "Complete"

class FormFieldType(Enum):
    text = "text"
    date = "date"
    checkbox = "checkbox"
    signature = "signature"
    undetermined = "undetermined"

class FormField(BaseModel):
    id: str
    name: str
    description: str
    form_field_type: FormFieldType
    bounding_box: List[int] = []
    page: int = -1
    mapping: List[int] = []

class FilledOutPackage(BaseModel):
    id: str
    email: str
    filled_out_pdf_id: str = ''

class TypeformResponse(BaseModel):
    id: str
    answers: List[Dict[str, Any]]

class Package(BaseModel):
    id: str
    name: str
    status: PackageStatus
    original_pdf_id: str
    original_image_ids: List[str] # In order of pages
    images_with_boxes_ids: List[str]
    typeform_json_schema: Dict[str, Any]
    form_fields: List[FormField]
    final_form: List[FormField]
    filled_out_packages: List[FilledOutPackage]
    typeform_url: str
    typeform_id: str
