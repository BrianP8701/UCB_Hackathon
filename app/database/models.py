from typing import List
from pydantic import BaseModel


class PackageModel(BaseModel):
    id: str
    name: str
    status: str
    original_pdfs_paths: List[str]
    images_with_boxes_paths: List[str]
    form_fields: List[str]
    filled_out_packages: List[str]
    google_form_url: str
