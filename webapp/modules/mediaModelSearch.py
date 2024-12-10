class MediaModelSearch:
    
    def __init__(self, mediaObj:dict):
        self.mediaObj = mediaObj
    
    def build(self, category:str, id:str, title:str, description:str, poster_path:str, score:float, release_year:str):
        return {
            "category": category,
            "id": id,
            "title": title,
            "description": description,
            "poster_path": poster_path,
            "score": score,
            "release_year": release_year
        }