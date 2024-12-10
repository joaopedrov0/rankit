from .mediaModelPage import MediaModelPage

from datetime import datetime

class BookModelPage(MediaModelPage):
    
    def __init__(self, mediaObj:dict):
        super().__init__(mediaObj)
    
    def build(self):
        mediaObj:dict = self.mediaObj
        publishedDate:str = None
        tags:list = None
        if mediaObj["volumeInfo"].get("publishedDate"):
            temp:list = mediaObj["volumeInfo"]["publishedDate"].split('-')
            publishedDate = temp[0]
            # publishedDate = "/".join(temp)
        if mediaObj["volumeInfo"].get("categories"):
            tags = []
            for tag in mediaObj["volumeInfo"]["categories"]:
                tags.append({"name": tag})
        mediaObj = {
            "category": "book",
            "id": mediaObj.get("id"),
            "title": mediaObj["volumeInfo"].get("title"),
            "description": mediaObj["volumeInfo"].get("description").replace('<b>', '').replace('</b>', '').replace('<p>', '').replace('</p>', '').replace('<i>', '').replace('</i>', '').replace('<br>', ''),
            "poster_path": mediaObj["volumeInfo"]["imageLinks"]["thumbnail"] if mediaObj["volumeInfo"].get("imageLinks").get("thumbnail") else None,
            "score": mediaObj["volumeInfo"].get("averageRating"),
            "release_year": publishedDate if publishedDate else None,
            "banner_path": None,
            "genre": tags,
            "size": mediaObj["volumeInfo"]["pageCount"] if mediaObj["volumeInfo"].get("pageCount") else None,
            }
        return mediaObj
    
   