"""MCP server implementation for object detection."""

import logging
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
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Set up server handlers."""

        @self.server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            """Return list of available tools."""
            return [
                types.Tool(
                    name="detect_objects",
                    description="Detect objects in an image and return bounding boxes with labels",
                    inputSchema={
                        "type": "object",
                        "properties": {"image_path": {"type": "string", "description": "Path to the image file"}},
                        "required": ["image_path"],
                    },
                )
            ]

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
            """Handle tool execution."""
            if name != "detect_objects":
                raise ValueError(f"Unknown tool: {name}")

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
