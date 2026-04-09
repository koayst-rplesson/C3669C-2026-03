# References:
# https://composio.dev/blog/how-to-effectively-use-prompts-resources-and-tools-in-mcp
# https://medium.com/@cstroliadavis/building-mcp-servers-315917582ad1

# fastmcp = 3.2.2
# python >= 3.10

from datetime import datetime
from fastmcp import FastMCP
from typing import Any, Dict, List, Optional
from zoneinfo import ZoneInfo

import json

# Create a server instance
mcp = FastMCP(name="My MCP Server")

# Sample data storage (in a real server, this might be a database)
SAMPLE_DATA = {
    "users": [
        {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "admin"},
        {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "user"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com", "role": "user"}
    ],
    "documents": {
        "readme": "Welcome\nThis is a sample document stored in the MCP server.",
        "config": '{"theme": "dark", "language": "en", "notifications": true}',
        "logs": "2025-08-14 10:00:00 - Server started\n2024-01-01 10:01:00 - User logged in"
    }
}

PORT = 8000

# =============================================================================
# RESOURCES - Data that clients can read
# =============================================================================

@mcp.resource("config://app-settings")
async def get_app_settings() -> str:
    """
    Application configuration settings.
    """
    return SAMPLE_DATA["documents"]["config"]

@mcp.resource("docs://readme")
async def get_readme() -> str:
    """
    Application readme documentation.
    """
    return SAMPLE_DATA["documents"]["readme"]

@mcp.resource("logs://server")
async def get_server_logs() -> str:
    """
    Server activity logs.
    """
    return SAMPLE_DATA["documents"]["logs"]

@mcp.resource("data://users")
async def get_users_data() -> str:
    """
    User database in JSON format.
    """
    return json.dumps(SAMPLE_DATA["users"], indent=2)


# =============================================================================
# RESOURCE TEMPLATES - Allow clients to request resources whose content depends 
#                     on parameters embedded in the URI.
#
# RREFERENCE - https://gofastmcp.com/servers/resources
#            - Resource Templates allow clients to request resources whose 
#              content depends on parameters embedded in the URI. Define a 
#              template using the same @mcp.resource decorator, but include 
#              {parameter_name} placeholders in the URI string and add 
#              corresponding arguments to your function signature.
# =============================================================================

@mcp.resource("user://{user_id}")
async def get_user_profile(user_id: str) -> str:
   """
   Fetches a user profile given a user_id.
   Resource template demonstrates how clients can call parameterized URIs.

   Args:
      user_id: ID of the user
   """
   if user_id.isdigit():
      user = [u for u in SAMPLE_DATA["users"] if u["id"] == int(user_id)]
      return json.dumps(user if user else {"error" : "User not found."}, indent=2)


# =============================================================================
# TOOLS - Functions that clients can call
# =============================================================================

@mcp.tool()
def add (a: float = 1.0, b: float = 1.0) -> float:
   """
    Add two numbers.

    Args:
       a: first float number (default: 1.0)
       b: second float number (default: 1.0)
   """
   return a + b

@mcp.tool()
def substract (a: float = 1.0, b: float = 1.0) -> float:
   """
    Substract two numbers.

    Args:
       a: first float number (default: 1.0)
       b: second float number (default: 1.0)
   """
   return a - b

@mcp.tool()
def multiply(a: float = 1.0, b: float = 1.0) -> float:
    """
    Multiply two numbers.

    Args:
       a: first float number (default: 1.0)
       b: second float number (default: 1.0)
    """
    return a * b

@mcp.tool()
def divide(a: float = 1.0, b: float = 1.0) -> float:
   """
    Divide number a by number b.

    Args:
       a: first float number (default: 1.0)
       b: second float number (default: 1.0)
   """
   if b == 0:
      raise ValueError("Division by zero")

   return a / b

@mcp.tool()
def get_current_time(format: str = "%Y-%m-%d %I:%M:%S %p", zoneinfo: str = "Asia/Singapore") -> str:
    """
    Get the current date and time.
    
    Args:
        format: Time format string (default: "%Y-%m-%d %I:%M:%S %p")
        zoneinfo: time zone string (default: "Asia/Singapore")
    
    Returns:
        Current time as formatted string
    """
    return datetime.now(ZoneInfo(zoneinfo)).strftime(format)


# =============================================================================
# PROMPTS - Reusable prompt template
# =============================================================================

@mcp.prompt()
async def explain_topic(topic : str = "Generative AI") -> str:
    """
    Generates a query prompt for explanation of topic.

    Args:
       topic: The topic (in string) to be explained (default: "Generative AI")
    """
    return f"Can you explain {topic} in a beginner friendly manner with simple wordings and no technical jargon. Include Concept & Examples."


# =============================================================================


if __name__ == "__main__":
   # Default: uses STDIO transport
   # Best for local tools and command-line scripts.
   #mcp.run()

   # Streamable HTTP: Recommended for web deployments. 
   mcp.run(transport="http", host="0.0.0.0", port=PORT)

   # SSE: For compatibility with existing SSE clients.
   # DO NOT USE SSE TRANSPORT: Deprecated as of MCP specification version 2025-03-26
   # https://mcp-framework.com/docs/Transports/sse/
   #mcp.run(transport="sse", host="127.0.0.1", port=8000)


