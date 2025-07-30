"""Test script for object detection with visualization."""

import json
import os

from src.detector import ObjectDetector


def test_detection_with_visualization() -> None:
    """Test object detection with visualization feature."""
    detector = ObjectDetector()

    # Test with the provided image
    image_path = "images/test.png"
    output_dir = "static/output"
    
    print(f"Testing detection with visualization on: {image_path}")

    try:
        # Test detect_and_draw method
        result = detector.detect_and_draw(image_path, output_dir, confidence_threshold=0.5)
        
        print(f"\nVisualization test completed!")
        print(f"Total objects detected: {result['total_objects']}")
        print(f"Confidence threshold: {result['confidence_threshold']}")
        print(f"Output image saved to: {result['output_path']}")
        
        print(f"\nDetected objects:")
        for i, detection in enumerate(result['detections'], 1):
            print(f"{i}. {detection['label']} (confidence: {detection['confidence']:.2f})")
            print(f"   Location: x={detection['bbox']['x']}, y={detection['bbox']['y']}")
            print(f"   Size: {detection['bbox']['width']}x{detection['bbox']['height']}")
        
        # Verify output file exists
        if os.path.exists(result['output_path']):
            print(f"\n✓ Output image file created successfully: {result['output_path']}")
        else:
            print(f"\n✗ Output image file not found: {result['output_path']}")
        
        # Print JSON format
        print("\n" + "="*50)
        print("JSON output:")
        print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_detection_with_visualization()