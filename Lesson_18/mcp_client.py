
# mcp_client.py
# This script demonstrates how to use FastMCP Client to call a tool on an MCP server.

# fastmcp = 3.2.2
# python >= 3.10

from fastmcp import Client  # Import the FastMCP Client class

# Create a client instance to connect to the MCP server
client = Client("mcp_server.py") 

# Asynchronous function to call the 'greet' tool on the server
async def call_tool(name: str): 
    async with client: 
        # Call the 'greet' tool with the provided name
        result = await client.call_tool("greet", {"name": name}) 
            
        # Print the result returned by the tool
        print(result.data) 

# Run the async function to call the tool with the name 'John'
import asyncio
asyncio.run(call_tool("John"))
