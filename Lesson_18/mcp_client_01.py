# References:
# https://www.datacamp.com/tutorial/building-mcp-server-client-fastmcp

# fastmcp = 3.2.2
# python >= 3.10

import asyncio
import pprint
import json

from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

SERVER_URL = "http://localhost:8000/mcp"

pp = pprint.PrettyPrinter(indent=2, width=100)

def unwrap_tool_result(resp):
    """
    Safely unwraps the content from a FastMCP tool call result object.
    """
    if hasattr(resp, "content") and resp.content:
        # The content is a list containing a single content object
        content_object = resp.content[0]
        # It could be JSON or plain text
        if hasattr(content_object, "json"):
            return content_object.json
        if hasattr(content_object, "text"):
            try:
                # Use ast.literal_eval for safely evaluating a string containing a Python literal
                return ast.literal_eval(content_object.text)
            except (ValueError, SyntaxError):
                # If it's not a literal, return the raw text
                return content_object.text
    return resp

async def main():
   transport = StreamableHttpTransport(url = SERVER_URL)
   client = Client(transport)

   print("\n🚀 Connecting to FastMCP server at:", SERVER_URL)

   async with client:
      # Ping to test connectivity
      print("\n🔗 Testing server connectivity...")
      await client.ping()
      print("✅ Server is reachable! ✅\n")

      # Discover server capabilities
      print("🛠️ Available tools:")
      pp.pprint(await client.list_tools())
      
      print("\n📚 Available resources:")
      pp.pprint(await client.list_resources())

      print("\n📚 Available resource templates:")
      pp.pprint(await client.list_resource_templates())
      
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
      print("\n🔍 Fetching resource: readme")
      res = await client.read_resource("docs://readme")
      print(res[0].text)

      # -----------------------------------------------------------------------------

      print("\n🔍 Fetching resource: logs")
      res = await client.read_resource("logs://server")
      print(res[0].text)

      # -----------------------------------------------------------------------------

      print("\n🔍 Fecthing resource: user data")
      res = await client.read_resource("data://users")
      print(json.dumps(json.loads(res[0].text), indent=2))

      # =============================================================================
      # RESOURCE TEMPLATE
      # =============================================================================
      
      print("\n🔍 Fteching resource: user profile #1")
      res = await client.read_resource("user://1")
      print(json.dumps(json.loads(res[0].text), indent=2))


      # =============================================================================
      # TOOLS
      # =============================================================================

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

      print("\n🛠️ get current time")
      zoneinfo = "Singapore"
      result = await client.call_tool(
         "get_current_time",
         {"zoneinfo" : zoneinfo}
      )
      print(f"The current time of {zoneinfo} is {result.content[0].text}")


      # =============================================================================
      # PROMPT
      # =============================================================================

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
    asyncio.run(main())