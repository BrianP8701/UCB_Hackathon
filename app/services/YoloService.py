import cv2
from typing import List
import logging

from app.services.yolo_v8.YOLOv8 import YOLOv8
from ultralytics import YOLO

class YoloService:
    def __init__(self) -> None:
        self.yolov8_detector = YOLOv8("best.onnx", conf_thres=0.5, iou_thres=0.3)

    def predict(self, img_path) -> List[List[int]]:
        img = cv2.imread(img_path)
        boxes, scores, class_ids = self.yolov8_detector(img)

        if(len(boxes) == 0):
            return [[]]

        return [[int(x) for x in box] for box in boxes]

    @classmethod
    def export_raw_weights_to_onnx(cls, path_to_model: str):
        model = YOLO(path_to_model) 
        model.export(format="onnx")


# Example of usage
if __name__ == "__main__":
    from app.services.PdfService import PdfService
    from app.services.PackageService import PackageService
    pdfService = PdfService()
    packageService = PackageService()
    # YoloService.export_raw_weights_to_onnx("/Users/brianprzezdziecki/Code/UCB_Hackathon/best.pt")
    yoloService = YoloService()
    preds = yoloService.predict("data/raw/jpgs/irs_forms/f433aois-pdf_6.jpeg")
    print(preds)
    img = cv2.imread("data/raw/jpgs/irs_forms/f433aois-pdf_6.jpeg")
    img = packageService.draw_bounding_boxes_on_image(img, preds)
    print(type(img))
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
