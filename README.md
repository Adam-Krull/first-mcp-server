# first-mcp-server

## Purpose
The purpose of this project is to create, host, and access an MCP server locally. The MCP server houses resources and tools that allow access to US Census Bureau data I collected about 5 states.

## Technologies used
The following Python libraries are critical to the project:
- [asyncio](https://docs.python.org/3/library/asyncio.html) - runs my server and makes my requests asynchronously
- [fastmcp](https://gofastmcp.com/getting-started/welcome) - creates the MCP server in a similar fashion to how fastapi creates python backends
- [langchain-mcp-adapters](https://github.com/langchain-ai/langchain-mcp-adapters) - defines the client I use to retrieve tools from the server
- [langgraph](https://www.langchain.com/langgraph) - provides the prebuilt agent I use to bind and call tools from my MCP server

## Result
Here is output I received for the last question (What are similar cities to Richardson?):

>Here are the three most similar cities to Richardson (based on cosine similarity):
>
>- Ogden, Utah
>- Thornton, Colorado
>- Round Rock, Texas
>
>Would you like more details on any of these cities (e.g., population, climate, cost of living) or prefer I compare Richardson to other states or the country as a whole?

The agent returns a complete response using the information from the tool call. A complete agent with a looping graph would allow me to continue the conversation.