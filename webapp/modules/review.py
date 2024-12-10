from .media import Media
from datetime import datetime, date
from .dbElementsAbstract import DBElementsAbstract

class Review(DBElementsAbstract):
    
    @staticmethod
    def generateReviewId(origin:str, category:str, mediaId:str):
        return "{}_{}_{}".format(origin, category, mediaId)
    
    def __init__(self, user_origin:str, category:str, mediaId:str, content:dict={}, realDate:str=None, strDate:str=None):
        self._id = Review.generateReviewId(user_origin, category, mediaId)
        self.user_origin = user_origin
        self.mediaTarget = Media.generateMediaId(category, mediaId)
        self.content = content
        self.realDate = realDate if realDate else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.strDate = strDate if strDate else date.today().strftime("%d/%m/%Y")
        
        
    def toDict(self):
        return {
            "_id": self._id,
            "user_origin": self.user_origin,
            "mediaTarget": self.mediaTarget,
            "content": self.content,
            "realDate": self.realDate,
            "strDate": self.strDate
        }