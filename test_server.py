"""Test MCP server startup."""

import asyncio
import json
import sys

async def test_server():
    """Test server by sending initialize request."""
    # Send initialize request
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }
    
    print(json.dumps(request))
    print("")  # Empty line to signal end of message
    sys.stdout.flush()
    
    # Wait a bit for response
    await asyncio.sleep(1)
    
    # Send list tools request
    request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    
    print(json.dumps(request))
    print("")
    sys.stdout.flush()
    
    await asyncio.sleep(1)

if __name__ == "__main__":
    print("Testing MCP server communication...", file=sys.stderr)
    asyncio.run(test_server())