from .mediaModelPage import MediaModelPage

class MovieModelPage(MediaModelPage):
    
    def __init__(self, mediaObj:dict):
        super().__init__(mediaObj)
    
    def build(self):
        mediaObj:dict = self.mediaObj
        temp_size:str = str(mediaObj["runtime"]) + 'm' if mediaObj["runtime"] < 60 else (str(mediaObj["runtime"]//60) + 'h' + str(mediaObj["runtime"]%60) + 'm')
        mediaObj = {
            "category": "movie",
            "id": mediaObj["id"],
            "title": mediaObj["title"],
            "description": mediaObj["overview"],
            "poster_path": "https://image.tmdb.org/t/p/w300_and_h450_bestv2{}".format(mediaObj["poster_path"]) if mediaObj["poster_path"] else None,
            "score": mediaObj["vote_average"],
            "release_year": str(mediaObj["release_date"])[0:4:1],
            "banner_path": "https://image.tmdb.org/t/p/w1920_and_h1080_bestv2{}".format(mediaObj["backdrop_path"]) if mediaObj["backdrop_path"] else None,
            "genre": mediaObj["genres"],
            "size": {
                        "time": temp_size
                    },
            }
        return mediaObj