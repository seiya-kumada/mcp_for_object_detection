"""Object detection logic using YOLOv8."""

import os
from typing import Any, Dict, List

import cv2
from ultralytics import YOLO


class ObjectDetector:
    """YOLOv8-based object detector."""

    def __init__(self, model_name: str = "yolov8n.pt"):
        """Initialize the detector with specified model.

        Args:
            model_name: YOLOv8 model name (default: yolov8n.pt for nano version)
        """
        self.model = YOLO(model_name)

    def detect(self, image_path: str) -> List[Dict[str, Any]]:
        """Detect objects in an image.

        Args:
            image_path: Path to the image file

        Returns:
            List of detected objects with bounding boxes and labels

        Raises:
            FileNotFoundError: If image file doesn't exist
            ValueError: If image format is invalid
        """
        # Check if file exists
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        # Check if file is valid image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Invalid image format: {image_path}")

        # Run detection (verbose=False to suppress output)
        results = self.model(image_path, verbose=False)

        # Process results
        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].tolist()

                    # Calculate x, y, width, height format
                    x = int(x1)
                    y = int(y1)
                    width = int(x2 - x1)
                    height = int(y2 - y1)

                    # Get class name
                    class_id = int(box.cls[0])
                    label = self.model.names[class_id]

                    # Get confidence score
                    confidence = float(box.conf[0])

                    detection = {
                        "label": label,
                        "bbox": {"x": x, "y": y, "width": width, "height": height},
                        "confidence": confidence,
                    }
                    detections.append(detection)

        return detections
