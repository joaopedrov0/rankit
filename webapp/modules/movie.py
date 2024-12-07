from .media import Media

class Movie(Media):
    
    def __init__(self, api_id, category, name, description, score, posterPath, bannerPath, originCountry, releaseDate, director, length, viewsList=..., realDate=None, strDate=None, ):
        super().__init__(api_id, category, name, description, score, posterPath, bannerPath, originCountry, releaseDate, viewsList, realDate, strDate)
        self.director = director
        self.length = length

    def toDict(self):
        """Converte a obra pra um dicionário (pra poder colocar no db 😉)"""

        return {
            "_id": self._id,
            "api_id": self.api_id,
            "category": self.category,
            "name": self.name,
            "description": self.description,
            "director": self.director,
            "length": self.length,
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