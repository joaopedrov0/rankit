from .mediaModelSearch import MediaModelSearch

from datetime import datetime

class GameModelSearch(MediaModelSearch):
    
    def __init__(self, mediaObj):
        super().__init__(mediaObj)
    
    def build(self):
        mediaObj = self.mediaObj
        mediaObj = {
            "category": "game",
            "id": mediaObj.get("id"),
            "title": mediaObj.get("name"),
            "description": mediaObj.get("summary"),
            "poster_path": "https://images.igdb.com/igdb/image/upload/t_cover_big/{}.jpg".format(mediaObj["cover"]["image_id"]) if mediaObj.get("cover") else None,
            "score": mediaObj.get("rating"),
            "release_year": datetime.fromtimestamp(mediaObj["first_release_date"]).year if mediaObj.get("first_release_date") else None,
            }
        return mediaObj