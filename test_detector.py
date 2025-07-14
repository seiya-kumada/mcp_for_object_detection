"""Test script for object detector."""

import json

from src.detector import ObjectDetector


def test_detection() -> None:
    """Test object detection with sample image."""
    detector = ObjectDetector()

    # Test with the provided image
    image_path = "images/test.png"
    print(f"Testing detection on: {image_path}")

    try:
        detections = detector.detect(image_path)

        print(f"\nFound {len(detections)} objects:")
        for i, detection in enumerate(detections):
            print(f"\n{i + 1}. {detection['label']} (confidence: {detection['confidence']:.2f})")
            print(f"   Location: x={detection['bbox']['x']}, y={detection['bbox']['y']}")
            print(f"   Size: {detection['bbox']['width']}x{detection['bbox']['height']}")

        # Print JSON format
        print("\nJSON output:")
        print(json.dumps({"detections": detections}, indent=2))

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_detection()
