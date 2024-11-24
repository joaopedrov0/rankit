class Media():
    def __init__(self, api, api_id, category, name, description, score, posterPath, bannerPath, originCountry, releaseDate, viewsList=[], reviews={}):
        self.api = api
        self.api_id = api_id
        self.category = category
        self.name = name
        self.description = description
        self.score = score
        self.posterPath = posterPath
        self.bannerPath = bannerPath
        self.originCountry = originCountry # País de origem
        self.releaseDate = releaseDate # Data de lançamento
        self.viewsList = viewsList
        self.viewsNumber = len(viewsList)
        self.reviews = reviews # {"owener_id": review_object ou review_id}
        
    def toDict(self):
        """Converte a obra pra um dicionário (pra poder colocar no db 😉)""" # abstractmethod vindo de DBElementsInterface

        return {
            "api": self.api,
            "api_id": self.api_id,
            "category": self.category,
            "name": self.name,
            "description": self.description,
            "score": self.score,
            "posterPath": self.posterPath,
            "bannerPath": self.bannerPath,
            "originCountry": self.originCountry,
            "releaseDate": self.releaseDate,
            "viewsList": self.viewsList,
            "viewsNumber": self.viewsNumber,
            "reviews": self.reviews,
        }