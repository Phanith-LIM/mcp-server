from fastmcp import FastMCP
from tools import sql_tool_mcp
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

mcp = FastMCP(name="FastMCP Server")
custom_middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"]),
]
mcp.mount("/sql_tool", sql_tool_mcp)
mcp_app = mcp.http_app(
    path='/mcp',
    transport='sse',
    middleware=custom_middleware,
)
