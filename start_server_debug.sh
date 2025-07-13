#!/bin/bash
echo "Starting MCP Object Detection Server..." >> /tmp/mcp_object_detection.log
echo "Date: $(date)" >> /tmp/mcp_object_detection.log
echo "PWD: $(pwd)" >> /tmp/mcp_object_detection.log
echo "PATH: $PATH" >> /tmp/mcp_object_detection.log

cd /Users/kumada/Projects/mcp_for_object_detection
/Users/kumada/.local/bin/uv run python -m src 2>> /tmp/mcp_object_detection.log