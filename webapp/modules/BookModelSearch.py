from .mediaModelSearch import MediaModelSearch

from datetime import datetime

class BookModelSearch(MediaModelSearch):
    
    def __init__(self, mediaObj:dict):
        super().__init__(mediaObj)
    
    def build(self):
        mediaObj:dict = self.mediaObj
        publishedDate:str = None
        if mediaObj["volumeInfo"].get("publishedDate"):
            temp:list = mediaObj["volumeInfo"]["publishedDate"].split('-')
            publishedDate = temp[0]
            # publishedDate = "/".join(temp)
        mediaObj = {
            "category": "book",
            "id": mediaObj.get("id"),
            "title": mediaObj["volumeInfo"].get("title"),
            "description": mediaObj["volumeInfo"].get("description"),
            "poster_path": mediaObj["volumeInfo"]["imageLinks"]["thumbnail"] if mediaObj["volumeInfo"].get("imageLinks") and mediaObj["volumeInfo"].get("imageLinks").get("thumbnail") else None,
            "score": mediaObj["volumeInfo"].get("averageRating"),
            "release_year": publishedDate if publishedDate else None,
            }
        return mediaObj