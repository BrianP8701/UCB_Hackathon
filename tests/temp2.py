import cv2
import asyncio

from app.services.PackageService import PackageService



image_path = 'storage/3c563012-ec2c-4e60-9197-5c2219512c3d.jpeg'

image = cv2.imread(image_path)

image = asyncio.run(PackageService.draw_bounding_boxes_on_image(image, [[1116, 937, 1842, 1032]]))

print(type(image))