"""Object detection logic using YOLOv8."""

import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np
from ultralytics import YOLO


class ObjectDetector:
    """YOLOv8-based object detector."""

    def __init__(self, model_name: str = "yolov8n.pt"):
        """Initialize the detector with specified model.

        Args:
            model_name: YOLOv8 model name (default: yolov8n.pt for nano version)
        """
        self.model = YOLO(model_name)

        # Color palette for bounding boxes (BGR format for OpenCV)
        self.colors = [
            (255, 0, 0),  # Blue
            (0, 255, 0),  # Green
            (0, 0, 255),  # Red
            (255, 255, 0),  # Cyan
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Yellow
            (128, 0, 128),  # Purple
            (255, 165, 0),  # Orange
            (0, 128, 255),  # Light Blue
            (255, 192, 203),  # Pink
        ]

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

    def detect_and_draw(self, image_path: str, output_dir: str, confidence_threshold: float = 0.5) -> Dict[str, Any]:
        """Detect objects and create annotated image.

        Args:
            image_path: Path to the image file
            output_dir: Directory to save the annotated image
            confidence_threshold: Minimum confidence score to display objects

        Returns:
            Dictionary containing detection results and output image path

        Raises:
            FileNotFoundError: If image file doesn't exist
            ValueError: If image format is invalid
        """
        # Perform detection
        detections = self.detect(image_path)

        # Filter detections by confidence threshold
        filtered_detections = [d for d in detections if d["confidence"] >= confidence_threshold]

        # Create annotated image
        output_path = self._create_annotated_image(image_path, filtered_detections, output_dir)

        return {
            "detections": filtered_detections,
            "output_path": output_path,
            "total_objects": len(filtered_detections),
            "confidence_threshold": confidence_threshold,
        }

    def _create_annotated_image(self, image_path: str, detections: List[Dict[str, Any]], output_dir: str) -> str:
        """Create annotated image with bounding boxes and labels.

        Args:
            image_path: Path to the original image
            detections: List of detection results
            output_dir: Directory to save the annotated image

        Returns:
            Path to the saved annotated image
        """
        # Create output directory
        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)

        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")

        # Draw bounding boxes and labels
        for i, detection in enumerate(detections):
            bbox = detection["bbox"]
            label = detection["label"]
            confidence = detection["confidence"]

            # Get coordinates
            x = bbox["x"]
            y = bbox["y"]
            w = bbox["width"]
            h = bbox["height"]

            # Select color based on object index
            color = self.colors[i % len(self.colors)]

            # Draw bounding box
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 1)

            # Prepare label text
            label_text = f"{label} {confidence:.2f}"

            # Get text size for background rectangle
            (text_width, text_height), baseline = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)

            # Draw label background
            cv2.rectangle(image, (x, y - text_height - baseline - 4), (x + text_width, y), (0, 0, 0), -1)

            # Draw label text
            cv2.putText(
                image,
                label_text,
                (x, y - baseline - 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (255, 255, 255),  # White text
                1,
            )

        # Generate output filename
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        input_filename = Path(image_path).stem
        output_filename = f"{input_filename}_detected_{timestamp}.jpg"
        output_path = output_dir_path / output_filename

        # Save annotated image
        cv2.imwrite(str(output_path), image)

        return str(output_path)
