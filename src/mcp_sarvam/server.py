import logging
from typing import Any
from collections.abc import Sequence
import mcp
from mcp.server import Server
from mcp.types import(
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource
)
from mcp.shared.exceptions import McpError
from mcp.server.lowlevel import NotificationOptions
from mcp.server.models import InitializationOptions
from . import tools

logger = logging.getLogger("mcp-sarvam")

server = Server("mcp-server-sarvam")

tool_handlers={}
def add_tool_handler(tool_class: tools.ToolHandler):
    global tool_handlers
    logger.debug(f"Registering tool handler: {tool_class.name}")
    tool_handlers[tool_class.name] = tool_class
    logger.debug(f"Registered tool handlers: {tool_handlers}")
    
def get_tool_handler(name: str) -> tools.ToolHandler | None:
    logger.debug(f"Looking for tool handler: {name}")
    if name not in tool_handlers:
        logger.warning(f"Tool Handler '{name}' not found.")
        return None
    return tool_handlers[name]

# Register
add_tool_handler(tools.CreateToolHandler_Translation())
add_tool_handler(tools.CreateToolHandler_LanguageIdentification())
add_tool_handler(tools.CreateToolHandler_Transliteration())

@server.list_tools()
async def list_tools() -> list[Tool]:
    logger.debug("Listing all available tools...")
    return [th.get_tool_description() for th in tool_handlers.values()]

@server.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    logger.info(f"Calling tool '{name}' with arguments {arguments}")
    
    if not isinstance(arguments, dict):
        logger.error("Arguments must be dictionary")
        raise RuntimeError("Arguments must be dictionary.")
    
    tool_handler = get_tool_handler(name)
    print(tool_handler)
    if not tool_handler:
        logger.error(f"Unknown tool: {name}")
        raise ValueError(f"Unknown tool: {name}")
    try:
        print(f"Running tool {name}")
        logger.debug(f"Running tool {name}")
        
        result = tool_handler.run_tool(arguments)

        return [TextContent(type='text',text=result)]
    except Exception as e:
        logger.error(f"Error running tool: {str(e)}")
        raise RuntimeError(f"Caught Exception. Error: {str(e)}")
    
async def run(read_stream, write_stream, iniitialization_options):
    logger.info("Starting Sarvam MCP Server.")
    await server.run(
        read_stream,
        write_stream,
        iniitialization_options
    )