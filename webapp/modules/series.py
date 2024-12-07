from .media import Media

class Series(Media):
    
    def __init__(self, api_id, category, name, description, score, posterPath, bannerPath, originCountry, releaseDate, director, seasons, episodes, viewsList=..., realDate=None, strDate=None):
        super().__init__(api_id, category, name, description, score, posterPath, bannerPath, originCountry, releaseDate, viewsList, realDate, strDate)
        self.director = director
        self.seasons = seasons
        self.episodes = episodes

    def toDict(self):
        """Converte a obra pra um dicionário (pra poder colocar no db 😉)"""

        return {
            "_id": self._id,
            "api_id": self.api_id,
            "category": self.category,
            "name": self.name,
            "description": self.description,
            "director": self.director,
            "seasons": self.seasons,
            "episodes": self.episodes,
            "score": self.score,
            "posterPath": self.posterPath,
            "bannerPath": self.bannerPath,
            "originCountry": self.originCountry,
            "releaseDate": self.releaseDate,
            "viewsList": self.viewsList,
            "viewsNumber": self.viewsNumber,
            "realDate": self.realDate,
            "strDate": self.strDate
        }