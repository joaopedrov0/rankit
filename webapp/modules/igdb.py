# from igdb.wrapper import IGDBWrapper
import requests
import json

import os
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv("IGDB_CLIENT_ID")
APPLICATION_ACCESS_TOKEN = os.getenv("IGDB_APPLICATION_ACCESS_TOKEN")
APPLICATION_AUTHORIZATION= 'Bearer {}'.format(APPLICATION_ACCESS_TOKEN)

if not CLIENT_ID or not APPLICATION_ACCESS_TOKEN:
    print("Alert: Missing authentication token for IGDB API")

class IGDB:
    
    @staticmethod
    def api_request(endpoint, query):
        url = "https://api.igdb.com/v4/{}".format(endpoint)
        headers = {
            "Authorization": APPLICATION_AUTHORIZATION,
            "Client-ID": CLIENT_ID,
        }
        data=query
        response = requests.post(url, headers=headers, data=data)
        content = response.content
        return json.loads(content.decode("utf-8"))
    
    def search(query):
        res = IGDB.api_request('games', 'search "{}";where category=0;fields name,cover.image_id,summary,rating,id,first_release_date;'.format(query))
        return res
    
    def getByID(id):
        res = IGDB.api_request('games', 'where id={};fields name,cover.image_id,artworks.image_id,summary,genres.name,themes.name,rating,id;'.format(id))
        return res[0]
