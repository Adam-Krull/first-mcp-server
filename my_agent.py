import asyncio

from langchain_mcp_adapters.tools import load_mcp_tools

from langgraph.prebuilt import create_react_agent

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

params = StdioServerParameters(
    command="python",
    args=["my_server.py"]
)

async def main():
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await load_mcp_tools(session)

            agent = create_react_agent("openai:gpt-5-nano", tools)
            response = await agent.ainvoke({"messages": "How does the median home price in Richardson compare to the median nationwide home price?"})
            print(response['messages'][-1].content)

if __name__ == "__main__":
    asyncio.run(main())