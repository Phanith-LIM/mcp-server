from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from server import mcp_app
import uvicorn


## FastAPI app
app = FastAPI(lifespan=mcp_app.lifespan, docs_url=None, redoc_url=None)
app.mount("/mcp-protocol", mcp_app)

## Routes
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>FastMCP Server</title>
        </head>
        <body>
            <p>MCP Server is now running!</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)