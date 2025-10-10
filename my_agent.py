import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient

from langgraph.prebuilt import create_react_agent

client = MultiServerMCPClient(
    {
        "census_bureau": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable_http"
        }
    }
)

async def main():
    tools = await client.get_tools()

    agent = create_react_agent("openai:gpt-5-nano", tools)
    #this one works!
    #response = await agent.ainvoke({"messages": "How does the median home price in Richardson compare to the median nationwide home price?"})
    #this one works if i specify Richardson and not Richardson, TX... i need to improve
    response = await agent.ainvoke({"messages": "What are similar cities to Richardson?"})
    print(response['messages'][-1].content)

if __name__ == "__main__":
    asyncio.run(main())