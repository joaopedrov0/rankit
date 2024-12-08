from .mediaModelPage import MediaModelPage

class AnimeModelPage(MediaModelPage):
    
    def __init__(self, mediaObj):
        super().__init__(mediaObj)
    
    def build(self):
        mediaObj = self.mediaObj
        print(mediaObj)
        temp_episode = 0
        if mediaObj.get('seasons'):
            for season in mediaObj["seasons"]:
                temp_episode += season["episode_count"]
        print(mediaObj["genres"])
        mediaObj = {
            "category": "anime",
            "id": mediaObj["id"],
            "title": mediaObj["name"],
            "description": mediaObj["overview"],
            "poster_path": "https://image.tmdb.org/t/p/w300_and_h450_bestv2{}".format(mediaObj["poster_path"]) if mediaObj["poster_path"] else None,
            "score": mediaObj["vote_average"],
            "release_year": str(mediaObj["first_air_date"])[0:4:1],
            "banner_path": "https://image.tmdb.org/t/p/w1920_and_h1080_bestv2{}".format(mediaObj["backdrop_path"]) if mediaObj["backdrop_path"] else None,
            "genre": mediaObj["genres"],
            "size": {
                        "seasons": len(mediaObj["seasons"]),
                        "episode_count": temp_episode
                    },
            }
        return mediaObj