from .media import Media

class Book(Media):
    
    def __init__(self, api_id, category, name, description, score, posterPath, bannerPath, originCountry, releaseDate, author, pages, viewsList=..., realDate=None, strDate=None, ):
        super().__init__(api_id, category, name, description, score, posterPath, bannerPath, originCountry, releaseDate, viewsList, realDate, strDate)
        self.author = author
        self.pages = pages

    def toDict(self):
        """Converte a obra pra um dicionário (pra poder colocar no db 😉)"""

        return {
            "_id": self._id,
            "api_id": self.api_id,
            "category": self.category,
            "name": self.name,
            "description": self.description,
            "author": self.author,
            "pages": self.pages,
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