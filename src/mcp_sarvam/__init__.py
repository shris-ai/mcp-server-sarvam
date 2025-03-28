import os
import logging
from dotenv import load_dotenv
from .server import run
import mcp
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger("mcp-sarvam")

load_dotenv()

api_key = os.getenv("SARVAM_API_KEY")
if not api_key:
    logger.error("Environment variable SARVAM_API_KEY not found in the environment.")
    raise ValueError("SARVAM_API_KEY environment variable is required.")
else:
    logger.info("Environment variable SARVAM_API_KEY is present in the environment.")
    
def main():
    """Main entry point for the package."""
    import asyncio
    import sys
    
    async def run_main():
        from mcp.server.stdio import stdio_server
        async with stdio_server() as (read_stream, write_stream):
            from .server import server as server_instance
            from mcp.server.models import InitializationOptions
            from mcp.server.lowlevel import NotificationOptions
            init_options = InitializationOptions(
                server_name="mcp-sarvam",
                server_version="0.0.1",
                capabilities=server_instance.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            )
            
            await run(read_stream, write_stream, init_options)
            
    asyncio.run(run_main())
    
__all__ = ['main', 'run']