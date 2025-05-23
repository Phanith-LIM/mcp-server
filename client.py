from mcp.client.stdio import StdioServerParameters
from smolagents import CodeAgent, LiteLLMModel, GradioUI
from smolagents.mcp_client import MCPClient

import os

if __name__ == "__main__":
    # mcp_server = StdioServerParameters(
    #     command= "npx",
    #     args= [
    #         "-y",
    #         "mcp-remote",
    #         "http://127.0.0.1:9000/mcp",
    #         "--allow-http",
    #     ],
    # )

    mcp_client = MCPClient(
        {
            "url":  "http://127.0.0.1:9000/mcp"
        }
   )

    tools = mcp_client.get_tools()
    for tool in tools:
        print(f"Tool: {tool.name}")

    model = LiteLLMModel(
        model_id='gemini/gemini-2.0-flash',
        api_key=os.environ.get('GOOGLE_API_KEY')
    )
    agent = CodeAgent(tools=[*tools], model=model)
    GradioUI(agent).launch(share=False)