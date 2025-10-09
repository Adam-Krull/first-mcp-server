import asyncio

from fastmcp import Client
from typing import Literal

client = Client("http://localhost:8000/mcp")

async def get_record(city: str):
    async with client:
        info = await client.read_resource(f"cities://{city}/info")
        print(info)

async def compare_city(city: str, region: Literal['state', 'country'], method: Literal['mean', 'median']):
    async with client:
        comparison = await client.call_tool('compare_city', {'city': city, 'region': region, 'method': method})
        print(comparison)

#asyncio.run(get_record('Richardson'))        
asyncio.run(compare_city('Richardson', 'state', 'median'))