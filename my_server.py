import asyncio
import numpy as np
import pandas as pd

from fastmcp import FastMCP
from typing import Literal

df = pd.read_csv('labeled.csv', index_col=0)
top_3 = np.load('top_3.npy').astype(int)

mcp = FastMCP("census_bureau")

@mcp.resource(
        uri="cities://{city}/info",
        name="city_information",
        description="Retrieves information about the city of your choice."
)
async def get_city_info(city: str) -> list:
    record = df[df['City'] == city].to_dict('records')
    return record

@mcp.tool(
        name="compare_city",
        description="Compares metrics from your city of choice to aggregate metrics for " \
        "its state or the country as a whole."
)
async def compare_city(city: str, region: Literal['state', 'country'] = 'country', method: Literal['mean', 'median'] = 'median') -> list:
    categories = ['Population', 'Percent employed', 'Occupation (MBSA)', 'Occupation (S)', 'Occupation (SO)', 
                  'Occupation (RCM)', 'Occupation (PT)', 'Median household income', 'Homeownership rate',
                  'Median home price', 'Median rent']
    sample = df[df['City'] == city]
    state = sample['State'].to_numpy()[0]
    if region == 'state':
        population = df[df['State'] == state][categories].agg(method)
        population['Region'] = state
    elif region == 'country':
        population = df[categories].agg(method)    
        population['Region'] = 'Country'

    population = pd.DataFrame(population).T.to_dict('records')
    final_list = [sample.to_dict('records')[0], population]
    return final_list    

@mcp.tool(
    name="find_similar_cities",
    description="Returns the three most similar cities to the one mentioned according to cosine similiarity."
)
async def find_similar(city: str) -> list:
    ind = df[df['City'] == city].index[0]
    top_3_inds = top_3[ind]
    top_3_info = df.iloc[top_3_inds]
    final_list = []
    for row in top_3_info.iterrows():
        city_state = f"{row[1]['City']}, {row[1]['State']}"
        final_list.append(city_state)
    return final_list
    
async def main():
    await mcp.run_async(
        transport="http",
        host="127.0.0.1",
        port=8000
    )

if __name__ == "__main__":
    asyncio.run(main())