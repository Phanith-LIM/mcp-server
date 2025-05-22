from fastmcp import FastMCP
from tools import sql_tool_mcp


app = FastMCP(name="FastMCP Server")

# Register the SQL tool
app.mount("/sql_tool", sql_tool_mcp)

if __name__ == "__main__":
    app.run(transport='streamable-http')