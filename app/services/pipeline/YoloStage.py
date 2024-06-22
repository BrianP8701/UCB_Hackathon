from app.types import *

def run_yolo_stage(package: Package):
    """
    Convert all files to images
    """
    original_pdf_paths: List[str] = package.original_pdf_paths
    