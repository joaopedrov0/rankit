from datetime import datetime, date
import bcrypt

from .dbElementsAbstract import DBElementsAbstract

class User(DBElementsAbstract):
    
    def __init__(self, 
                 name:str, 
                 username:str, 
                 email:str, 
                 password:str, 
                 icon:int=0, 
                 banner:int=0, 
                 bio:str='', 
                 followers:list=[], 
                 followersCount:int=0,
                 following:list=[], 
                 followingCount:int=0,
                 watched:dict={
                    "movie": {},
                    "serie": {},
                    "anime": {},
                    "game": {},
                    "book": {}
                },
                 watchedNumber:int=0,
                 watchList:dict={
                    "movie": {}, # {"media": True|False}
                    "serie": {},
                    "anime": {},
                    "game": {},
                    "book": {}
                },
                 watchListSize:int=0,
                 reviewsNumber:int=0,
                 diary:list=[],
                 favorites:dict={
                    "movie": [],
                    "serie": [],
                    "anime": [],
                    "game": [],
                    "book": []
                 },
                 realDate:str=None,
                 strDate:str=None,
                 config:dict={}):
        self.name:str = name # Nome qualquer
        self.username:str = username # Nome de usuário (único)
        self.icon:int = icon # Código do ícone
        self.banner:int = banner # Código do banner
        self.bio:str = bio # Bio (até 200 char)
        self.email:str = email # Email
        self.password:bytes =  self.hashpw(password)# Senha...
        self.followers:list = followers # Quem segue ele (lista de ids)
        self.followersCount:int = followersCount if followersCount else len(followers)
        self.following:list = following # Quem ele segue (lista de ids)
        self.followingCount:int = followingCount if followingCount else len(following)
        self.watched:dict = watched # Mídias que ele já assistiu, em ordem de preferência
        self.watchedNumber:int = watchedNumber
        self.watchList:dict = watchList # Mídias que pretende consumir // está assistindo {estado: pretende assistir | assistindo}
        self.watchListSize:int = watchListSize
        # self.reviews = reviews # Lista com códigos das reviews do usuário
        self.reviewsNumber:int = reviewsNumber
        self.diary:list = diary
        self.favorites:dict = favorites
        self.config:dict = config # Configurações de personalização do usuário
        self.realDate:str = realDate if realDate else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.strDate:str = strDate if strDate else date.today().strftime("%d/%m/%Y")
        
    def toDict(self):
        """Converte o usuário pra um dicionário (pra poder colocar no db 😉)"""
        return {
            "name": self.name,
            "username": self.username,
            "icon": self.icon,
            "banner": self.banner,
            "bio": self.bio,
            "email": self.email,
            "password": self.password,
            "followers": self.followers,
            "followersCount": self.followersCount,
            "following": self.following,
            "followingCount": self.followingCount,
            "watched": self.watched,
            "watchedNumber": self.watchedNumber,
            "watchList": self.watchList,
            "watchListSize": self.watchListSize,
            "reviewsNumber": self.reviewsNumber,
            "diary": self.diary,
            "favorites": self.favorites,
            "config": self.config,
            "strDate": self.strDate,
            "realDate": self.realDate
            
        }

    def hashpw(self, password:str): # retorna :bytes
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
