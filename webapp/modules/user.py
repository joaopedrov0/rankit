from datetime import datetime, date
import bcrypt

from .dbElementsAbstract import DBElementsAbstract

class User(DBElementsAbstract):
    
    def __init__(self, 
                 name, 
                 username, 
                 email, 
                 password, 
                 icon=0, 
                 banner=0, 
                 bio='', 
                 followers=[], 
                 followersCount=0,
                 following=[], 
                 followingCount=0,
                 watched={
                    "movie": {},
                    "serie": {},
                    "anime": {},
                    "game": {},
                    "book": {}
                },
                 watchedNumber=0,
                 watchList={
                    "movie": {}, # {"media": mediaObj, "watching:" True|False}
                    "serie": {},
                    "anime": {},
                    "game": {},
                    "book": {}
                },
                 watchListSize=0,
                 reviewsNumber=0,
                 diary=[],
                 favorites={
                    "movie": [],
                    "serie": [],
                    "anime": [],
                    "game": [],
                    "book": []
                 },
                 realDate=None,
                 strDate=None,
                 config={}):
        self.name = name # Nome qualquer
        self.username = username # Nome de usuário (único)
        self.icon = icon # Código do ícone
        self.banner = banner # Código do banner
        self.bio = bio # Bio (até 200 char)
        self.email = email # Email
        self.password =  self.hashpw(password)# Senha...
        self.followers = followers # Quem segue ele (lista de ids)
        self.followersCount = followersCount if followersCount else len(followers)
        self.following = following # Quem ele segue (lista de ids)
        self.followingCount = followingCount if followingCount else len(following)
        self.watched = watched # Mídias que ele já assistiu, em ordem de preferência
        self.watchedNumber = watchedNumber
        self.watchList = watchList # Mídias que pretende consumir // está assistindo {estado: pretende assistir | assistindo}
        self.watchListSize = watchListSize
        # self.reviews = reviews # Lista com códigos das reviews do usuário
        self.reviewsNumber = reviewsNumber
        self.diary = diary
        self.favorites = favorites
        self.config = config # Configurações de personalização do usuário
        self.realDate = realDate if realDate else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.strDate = strDate if strDate else date.today().strftime("%d/%m/%Y")
        
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

    def hashpw(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
