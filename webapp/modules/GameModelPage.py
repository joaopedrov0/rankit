from .mediaModelPage import MediaModelPage

from datetime import datetime

class GameModelPage(MediaModelPage):
    
    def __init__(self, mediaObj:dict):
        super().__init__(mediaObj)
    
    def build(self):
        mediaObj:dict = self.mediaObj
        tags:list = []
        if mediaObj.get('genres'):
            for genre in mediaObj["genres"]:
                # tags.append(genre["name"])
                tags.append(genre)
        if mediaObj.get('themes'):
            for theme in mediaObj["themes"]: # O(n)
                # tags.append(theme["name"])
                tags.append(theme)
        mediaObj = {
            "category": "game",
            "id": mediaObj.get("id"),
            "title": mediaObj.get("name"),
            "description": mediaObj.get("summary"),
            "poster_path": "https://images.igdb.com/igdb/image/upload/t_cover_big/{}.jpg".format(mediaObj["cover"]["image_id"]) if mediaObj.get("cover") else None,
            "score": "{:.2f}".format(mediaObj.get("rating")) if mediaObj.get("rating") else None,
            "release_year": str(datetime.fromtimestamp(mediaObj["first_release_date"]).year) if mediaObj.get("first_release_date") else None,
            "banner_path": "https://images.igdb.com/igdb/image/upload/t_1080p/{}.jpg".format(mediaObj["artworks"][0]["image_id"]) if mediaObj.get("artworks") else None,
            "genre": tags,
            "size": None,
            }
        return mediaObj
        # Pior Caso: O(n) | Melhor Caso: Ω(1)
    
   