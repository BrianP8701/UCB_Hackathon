from enum import Enum

class PackageStatus(Enum):
    detecting = "Detecting Form Boxes with YOLO"
    analyzing = "Analyzing Form Boxes With GPT4o"
    creating = "Creating Form with GPT4o"
    complete = "Complete"
