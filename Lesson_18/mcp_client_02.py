# mcp_client_02.py

# MCP Client Example
# This example demonstrates how to create a simple MCP client using FastMCP.
# It connects to the MCP server, retrieves resources, uses tools, and interacts with prompts.

# fastmcp = 2.12.2
# python >= 3.10

import asyncio
import pprint
import json

from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

# change the server URL accordingly
SERVER_URL = "https://hot-potato.fastmcp.app/mcp"

pp = pprint.PrettyPrinter(indent=2, width=100)

async def main():
   transport = StreamableHttpTransport(url = SERVER_URL)
   client = Client(transport, auth="fmcp_5Go_YOUR API KEY")

   print("\n🚀 Connecting to FastMCP server at:", SERVER_URL)

   async with client:
      # Ping to test connectivity
      print("\n🔗 Testing server connectivity...")
      await client.ping()
      print("✅ Server is reachable! ✅\n")

      # Discover server capabilities
      print("🛠️ Available tools:")
      pp.pprint(await client.list_tools())
      
      # List available resources
      print("\n📚 Available resources:")
      pp.pprint(await client.list_resources())

      # List available resource templates
      print("\n📚 Available resource templates:")
      pp.pprint(await client.list_resource_templates())
      
      # List available prompts
      print("\n💬 Available prompts:")
      pp.pprint(await client.list_prompts())

      # =============================================================================
      # RESOURCE
      # =============================================================================

      # Fetch the resources
      print("\n🔍 Fetching resource: configuration settings")
      res = await client.read_resource("config://app-settings")
      print(json.dumps(json.loads(res[0].text), indent=2))

      # -----------------------------------------------------------------------------

      # Fetch the readme document
      print("\n🔍 Fetching resource: readme")
      res = await client.read_resource("docs://readme")
      print(res[0].text)

      # -----------------------------------------------------------------------------

      # Fetch the server logs
      # Note: In a real server, logs might be sensitive information and should be handled with care.
      # Here we are just simulating the retrieval of logs.
      print("\n🔍 Fetching resource: logs")
      res = await client.read_resource("logs://server")
      print(res[0].text)

      # -----------------------------------------------------------------------------

      # Fetch the user data
      # Note: This is a sample data structure. In a real application, this would likely be fetched from a database.
      print("\n🔍 Fecthing resource: user data")
      res = await client.read_resource("data://users")
      print(json.dumps(json.loads(res[0].text), indent=2))

      # =============================================================================
      # RESOURCE TEMPLATE
      # =============================================================================
      
      # Fetch a specific user profile using the resource template
      print("\n🔍 Fetching resource: user profile #1")
      res = await client.read_resource("user://1")
      print(json.dumps(json.loads(res[0].text), indent=2))


      # =============================================================================
      # TOOLS
      # =============================================================================

      # Add two numbers using the tool
      print("\n🛠️ add")
      a = 1
      b = 2
      result = await client.call_tool(
         "add",
         {"a" : a, "b": b}
      )
      # take note the result text is a string
      print(f"{a} + {b} = {result.content[0].text}")
 
      # -----------------------------------------------------------------------------
      
      # Subtract two numbers using the tool
      print("\n🛠️ substract")
      a = 20
      b = 10
      result = await client.call_tool(
         "substract",
         {"a" : a, "b": b}
      )
      # take note the result text is a string
      print(f"{a} - {b} = {result.content[0].text}")

      # -----------------------------------------------------------------------------

      # Multiply two numbers using the tool
      print("\n🛠️ multiply")
      a = 8
      b = 6
      result = await client.call_tool(
         "multiply",
         {"a" : a, "b": b}
      )
      # take note the result text is a string
      print(f"{a} x {b} = {result.content[0].text}")

      # -----------------------------------------------------------------------------

      # Divide two numbers using the tool
      # Note: Division by zero will raise an exception, which we will handle.
      # This is a good example of how to handle errors in tool calls.   
      print("\n🛠️ divide")
      a = 88
      b = 10
      result = await client.call_tool(
         "divide",
         {"a" : a, "b": b}
      )
      # take note the result text is a string
      print(f"{a} / {b} = {result.content[0].text}")
 
      # -----------------------------------------------------------------------------

      print("\n🛠️ divide by zero")
      a = 88
      b = 0
      try:
         result = await client.call_tool(
            "divide",
            {"a" : a, "b": b}
         )
      except Exception as e:
         print(f"Tool Error: {e}")
      else:
         # take note the result text is a string
         print(f"{a} / {b} = {result.content[0].text}")

      # -----------------------------------------------------------------------------

      # Get the current time using the tool
      print("\n🛠️ get current time")
      zoneinfo = "Asia/Hong_Kong"
      result = await client.call_tool(
         "get_current_time",
         {"zoneinfo" : zoneinfo}
      )
      print(f"The current time of {zoneinfo} is {result.content[0].text}")


      # =============================================================================
      # PROMPT
      # =============================================================================

      # Get a prompt template
      print("\n🦜 get prompt template")
      topic = "Quantum Computing"
      prompt_resp = await client.get_prompt(
            "explain_topic", 
            {"topic": topic}
      )
      print("Generated prompt is:")
      for msg in prompt_resp.messages:
         print(f"{msg.role.upper()}: {msg.content.text}\n")


if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())
