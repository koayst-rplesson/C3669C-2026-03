# mcp_server.py
# This script sets up a Model Context Protocol (MCP) server using FastMCP.
#
# fastmcp = 3.2.2
# python >= 3.10

# Import the FastMCP library
from fastmcp import FastMCP  

# Create an MCP server instance with a custom name
mcp = FastMCP("My MCP Server")

# Register a tool with the MCP server that greets the user
@mcp.tool
def greet(name: str) -> str:
    """Return a greeting for the given name."""
    return f"Hello, {name}!"

# Start the MCP server if this script is run directly
if __name__ == "__main__":
    # The default transport is stdio
    mcp.run()
