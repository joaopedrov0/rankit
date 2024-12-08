from .mediaModelSearch import MediaModelSearch

class AnimeModelSearch(MediaModelSearch):
    
    def __init__(self, mediaObj):
        super().__init__(mediaObj)
    
    def build(self):
        mediaObj = self.mediaObj
        mediaObj = {
            "category": "anime",
            "id": mediaObj["id"],
            "title": mediaObj["name"],
            "description": mediaObj["overview"],
            "poster_path": "https://image.tmdb.org/t/p/w300_and_h450_bestv2{}".format(mediaObj["poster_path"]) if mediaObj["poster_path"] else None,
            "score": mediaObj["vote_average"],
            "release_year": str(mediaObj["first_air_date"])[0:4:1],
            }
        return mediaObj