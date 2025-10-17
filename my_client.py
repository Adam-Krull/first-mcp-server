#imports
import asyncio

from fastmcp import Client
from typing import Literal
#creating the client object using the local address
client = Client("http://localhost:8000/mcp")
#must define functions interacting with mcp server to be async
async def get_record(city: str):
    async with client:
        info = await client.read_resource(f"cities://{city}/info")
        print(info)
#function with limited options for arguments to match backend
async def compare_city(city: str, region: Literal['state', 'country'], method: Literal['mean', 'median']):
    async with client:
        comparison = await client.call_tool('compare_city', {'city': city, 'region': region, 'method': method})
        print(comparison)

#asyncio.run(get_record('Richardson'))        
asyncio.run(compare_city('Richardson', 'state', 'median'))