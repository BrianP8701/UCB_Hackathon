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

    def export_raw_weights_to_onnx(path_to_model: str):
        model = YOLO(path_to_model) 
        model.export(format="onnx")


# Example of usage
if __name__ == "__main__":
    yolo_service = YoloService()
    box = yolo_service.predict("/Users/brianprzezdziecki/Code/UCB_Hackathon/data/raw/jpgs/random/caaraz3-pdf_0.jpeg")
    print(box)
