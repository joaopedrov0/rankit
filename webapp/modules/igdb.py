# from igdb.wrapper import IGDBWrapper
import requests
import json

import os
from dotenv import load_dotenv
load_dotenv()

from typing import Type

CLIENT_ID = os.getenv("IGDB_CLIENT_ID")
APPLICATION_ACCESS_TOKEN = os.getenv("IGDB_APPLICATION_ACCESS_TOKEN")
APPLICATION_AUTHORIZATION= 'Bearer {}'.format(APPLICATION_ACCESS_TOKEN)

if not CLIENT_ID or not APPLICATION_ACCESS_TOKEN:
    print("Alert: Missing authentication token for IGDB API")

class IGDB:
    
    @staticmethod
    def api_request(endpoint:str, query:str):
        url:str = "https://api.igdb.com/v4/{}".format(endpoint)
        headers:dict = {
            "Authorization": APPLICATION_AUTHORIZATION,
            "Client-ID": CLIENT_ID,
        }
        data:str=query
        response:Type[requests.models.Response] = requests.post(url, headers=headers, data=data)
        content:bytes = response.content
        return json.loads(content.decode("utf-8"))
    
    @staticmethod
    def search(query:str):
        res:list = IGDB.api_request('games', 'search "{}";where category=(0,1,2,4,8,9,10);fields name,cover.image_id,summary,rating,id,first_release_date; limit 15;'.format(query))
        return res
    
    @staticmethod
    def getByID(id):
        res:list = IGDB.api_request('games', 'where id={};fields name,cover.image_id,artworks.image_id,summary,genres.name,themes.name,rating,id;'.format(id))
        return res[0]
