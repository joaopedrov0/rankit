from datetime import date, datetime
from .dbElementsAbstract import DBElementsAbstract

class Media(DBElementsAbstract):
    
    @staticmethod
    def generateMediaId(category, api_id):
        return "{}_{}".format(category, api_id)
    
    def __init__(self, api_id:str, category:str, name:str, description:str, score:float, posterPath:str, bannerPath:str, originCountry:str, releaseDate:str, viewsList:list=[], realDate:str=None, strDate:str=None):
        self._id:str = Media.generateMediaId(category, api_id)
        self.api_id = api_id
        self.category = category
        self.name = name
        self.description = description
        self.score = score
        self.posterPath = posterPath
        self.bannerPath = bannerPath
        self.originCountry = originCountry # País de origem
        self.releaseDate = releaseDate # Data de lançamento
        self.viewsList = viewsList # Lista de usuários que viram
        self.viewsNumber:int = len(viewsList)
        self.realDate = realDate if realDate else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.strDate = strDate if strDate else date.today().strftime("%d/%m/%Y")
        # self.reviews = reviews # {"owner_id": review_object ou review_id}
        
    def toDict(self):
        """Converte a obra pra um dicionário (pra poder colocar no db 😉)"""

        return {
            "_id": self._id,
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
            "realDate": self.realDate,
            "strDate": self.strDate
        }