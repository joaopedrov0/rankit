from .mediaModelSearch import MediaModelSearch

class MovieModelSearch(MediaModelSearch):
    
    def __init__(self, mediaObj):
        super().__init__(mediaObj)
    
    def build(self):
        mediaObj = self.mediaObj
        mediaObj = {
            "category": "movie",
            "id": mediaObj["id"],
            "title": mediaObj["title"],
            "description": mediaObj["overview"],
            "poster_path": "https://image.tmdb.org/t/p/w300_and_h450_bestv2{}".format(mediaObj["poster_path"]) if mediaObj["poster_path"] else None,
            "score": mediaObj["vote_average"],
            "release_year": str(mediaObj["release_date"])[0:4:1],
            }
        return mediaObj