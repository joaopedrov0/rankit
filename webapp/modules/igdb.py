# from igdb.wrapper import IGDBWrapper
import requests
import json

CLIENT_ID = 'zdrrwjhnfoul1c9ka7elgua55paq2h'
APPLICATION_ACCESS_TOKEN = 'svec0ee8vn445zl2rpktkitpu5jlms'
APPLICATION_AUTHORIZATION= 'Bearer {}'.format(APPLICATION_ACCESS_TOKEN)

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
