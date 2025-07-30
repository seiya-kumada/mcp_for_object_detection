"""MCP server implementation for object detection."""

import logging
import os
import shutil
import time
from pathlib import Path
from typing import Any

import mcp.server.stdio
from mcp import types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

from .detector import ObjectDetector

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ObjectDetectionServer:
    """MCP server for object detection."""

    def __init__(self) -> None:
        self.server = Server("object-detection")
        self.detector = ObjectDetector()
        self.static_dir = self._get_static_dir()
        self.input_dir = os.path.join(self.static_dir, "input")
        self.output_dir = os.path.join(self.static_dir, "output")
        
        # Create directories
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        self._setup_handlers()
    
    def _get_static_dir(self) -> str:
        """Get static files directory path."""
        current_dir = Path(__file__).parent.parent
        return os.path.join(current_dir, "static")

    def _setup_handlers(self) -> None:
        """Set up server handlers."""

        @self.server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            """Return list of available tools."""
            return [
                types.Tool(
                    name="detect_objects",
                    description="Detect objects in an image and return bounding boxes with labels (JSON only)",
                    inputSchema={
                        "type": "object",
                        "properties": {"image_path": {"type": "string", "description": "Path to the image file"}},
                        "required": ["image_path"],
                    },
                ),
                types.Tool(
                    name="detect_and_visualize",
                    description="Detect objects and create annotated image with bounding boxes and labels",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "image_path": {"type": "string", "description": "Path to the image file"},
                            "confidence_threshold": {"type": "number", "description": "Minimum confidence score (0.0-1.0)", "default": 0.5}
                        },
                        "required": ["image_path"],
                    },
                )
            ]

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
            """Handle tool execution."""
            try:
                if name == "detect_objects":
                    return await self._handle_detect_objects(arguments)
                elif name == "detect_and_visualize":
                    return await self._handle_detect_and_visualize(arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")
            except Exception as e:
                return [types.TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def _handle_detect_objects(self, arguments: dict[str, Any]) -> list[types.TextContent]:
        """Handle object detection (JSON only)."""
        image_path = arguments.get("image_path")
        if not image_path:
            raise ValueError("image_path is required")

        try:
            # Perform detection
            detections = self.detector.detect(image_path)
            
            # Format response
            result = {"detections": detections}
            
            return [types.TextContent(type="text", text=str(result))]

        except FileNotFoundError as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]
        except ValueError as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def _handle_detect_and_visualize(self, arguments: dict[str, Any]) -> list[types.TextContent]:
        """Handle object detection with visualization."""
        image_path = arguments.get("image_path")
        confidence_threshold = arguments.get("confidence_threshold", 0.5)
        
        if not image_path:
            raise ValueError("image_path is required")

        try:
            # Copy input image to input directory
            input_image_path = await self._copy_input_image(image_path)
            
            # Perform detection and create annotated image
            result = self.detector.detect_and_draw(input_image_path, self.output_dir, confidence_threshold)
            
            # Format response
            output_url = f"file:///{result['output_path'].replace(os.sep, '/')}"
            
            response_text = f"""物体検出結果

検出されたオブジェクト数: {result['total_objects']}
信頼度閾値: {result['confidence_threshold']}

検出詳細:
"""
            
            for i, detection in enumerate(result['detections'], 1):
                response_text += f"{i}. {detection['label']} (信頼度: {detection['confidence']:.2f})\n"
                response_text += f"   位置: x={detection['bbox']['x']}, y={detection['bbox']['y']}\n"
                response_text += f"   サイズ: {detection['bbox']['width']}x{detection['bbox']['height']}\n\n"
            
            response_text += f"\n結果画像: {output_url}"
            
            return [types.TextContent(type="text", text=response_text)]

        except FileNotFoundError as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]
        except ValueError as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def _copy_input_image(self, image_path: str) -> str:
        """Copy input image to input directory."""
        # Generate filename
        original_filename = os.path.basename(image_path)
        name, ext = os.path.splitext(original_filename)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        new_filename = f"{name}_{timestamp}{ext}"
        
        # Copy destination path
        dest_path = os.path.join(self.input_dir, new_filename)
        
        # Copy file
        shutil.copy2(image_path, dest_path)
        
        return dest_path

    async def run(self) -> None:
        """Run the MCP server."""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="object-detection",
                    server_version="0.1.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(), experimental_capabilities={}
                    ),
                ),
            )
