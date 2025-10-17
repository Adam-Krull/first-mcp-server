#imports
import asyncio
import numpy as np
import pandas as pd

from fastmcp import FastMCP
from typing import Literal
#resources for use by the server
df = pd.read_csv('labeled.csv', index_col=0)
top_3 = np.load('top_3.npy').astype(int)
#creating server object with name census_bureau
mcp = FastMCP("census_bureau")
#resource decorator with description
@mcp.resource(
        uri="cities://{city}/info",
        name="city_information",
        description="Retrieves information about the city of your choice."
)
#actual resource definition to get record in dictionary format
async def get_city_info(city: str) -> list:
    record = df[df['City'] == city].to_dict('records')
    return record
#tool decorator for city comparison tool
@mcp.tool(
        name="compare_city",
        description="Compares metrics from your city of choice to aggregate metrics for " \
        "its state or the country as a whole."
)
#tool function to compare city to aggregate metrics for state/country with default values
async def compare_city(city: str, region: Literal['state', 'country'] = 'country', method: Literal['mean', 'median'] = 'median') -> list:
    #list of column names from dataframe for metrics
    categories = ['Population', 'Percent employed', 'Occupation (MBSA)', 'Occupation (S)', 'Occupation (SO)', 
                  'Occupation (RCM)', 'Occupation (PT)', 'Median household income', 'Homeownership rate',
                  'Median home price', 'Median rent']
    #extract row for specified city and state name
    sample = df[df['City'] == city]
    state = sample['State'].to_numpy()[0]
    #if comparing to state, aggregate by state
    if region == 'state':
        population = df[df['State'] == state][categories].agg(method)
        population['Region'] = state
    #if comparing to country (default behavior), apply aggregate method to entire dataframe    
    elif region == 'country':
        population = df[categories].agg(method)    
        population['Region'] = 'Country'
    #recast the aggregate metrics as a dataframe and output as a dictionary
    population = pd.DataFrame(population).T.to_dict('records')
    #combine the two dictionaries for sample and population and return
    final_list = [sample.to_dict('records')[0], population]
    return final_list    
#tool decorator for similarity search function
@mcp.tool(
    name="find_similar_cities",
    description="Returns the three most similar cities to the one mentioned according to cosine similiarity."
)
#tool definition to find the three most similar cities to one listed
async def find_similar(city: str) -> list:
    #retrieve dataframe index of city
    ind = df[df['City'] == city].index[0]
    #use index to access 3 most similar cities in numpy array
    top_3_inds = top_3[ind]
    #use these indices to get information from dataframe
    top_3_info = df.iloc[top_3_inds]
    final_list = []
    #work through the dataframe and add city name and state to final list
    for row in top_3_info.iterrows():
        city_state = f"{row[1]['City']}, {row[1]['State']}"
        final_list.append(city_state)
    return final_list
#define main function to run mcp server asynchronously    
async def main():
    await mcp.run_async(
        transport="http",
        host="127.0.0.1",
        port=8000
    )

if __name__ == "__main__":
    asyncio.run(main())