import cv2
import asyncio
from pydantic import BaseModel, Field
from typing import List
import numpy as np
from PIL import Image
import io

from app.services.PdfService import PdfService
from app.services.PackageService import PackageService

pdf_path = 'data/raw/pdfs/irs_forms/f11c.pdf'

total_count, form_fields = PdfService.get_form_fields_and_rectangles(pdf_path)
print(total_count)

# # Seperate form fields by pages
# images = PdfService.convert_pdf_to_images(pdf_path)
# imgs = []
# for image_bytes in images:
#     image = Image.open(io.BytesIO(image_bytes))
#     image_np = np.array(image)
#     imgs.append(image_np)

# for i, img in enumerate(imgs):
#     this_pages_form_fields = form_fields[i]
#     bounding_boxes = [field[0] for field in this_pages_form_fields]

#     img = PackageService.draw_bounding_boxes_on_image(img, bounding_boxes)
#     cv2.imshow('image', img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
