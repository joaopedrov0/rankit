from pymongo import MongoClient
import bcrypt
import secrets
from datetime import date, datetime

# import webapp.modules as modules # Nossas classes estão aqui
# modules.DBElemensInterface.register(modules.User) # Registrando user como usuário da interface do db
# modules.DBElemensInterface.register(modules.Media) # mesma coisa com media

'''AVISO:
- Criei uma pasta modules e copiei todas as classes abaixo nela, além de classes que eu havia criado no outro repositório.
- Modificação feita por Nathan (19/11/24 - 10:00)'''

MONGODB_URI = 'mongodb+srv://rankit:rankitpass@master.jshtk.mongodb.net/?retryWrites=true&w=majority&appName=master' # URI pra conectar as parada

# Mongo Client
client = MongoClient(MONGODB_URI) # Cria o client q consegue fazer o crud

# Mongo Database

db = client.rankit

# Mongo Collections

## Users
UsersCollection = db.users

## Media
MediaCollection = db.media

## Reviews
ReviewsCollection = db.reviews

## Sessions
SessionsCollection = db.sessions

# Create your models here.

class User():
    
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
                    "movie": [],
                    "serie": [],
                    "anime": [],
                    "game": [],
                    "book": []
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
    
class Media():
    
    @staticmethod
    def generateMediaId(category, api_id):
        return "{}_{}".format(category, api_id)
    
    def __init__(self, api_id, category, name, description, score, posterPath, bannerPath, originCountry, releaseDate, viewsList=[], realDate=None, strDate=None):
        self._id = Media.generateMediaId(category, api_id)
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
        self.viewsNumber = len(viewsList)
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
        
class Review:
    
    @staticmethod
    def generateReviewId(origin, category, mediaId):
        return "{}_{}_{}".format(origin, category, mediaId)
    
    def __init__(self, user_origin, category, mediaId, content={}, realDate=None, strDate=None):
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
    

    
# newUser = User("RainanKaneka", "rainankaneka", "4", "0", "sim", "email.rainan@gmail.com", "12345")

# print(newUser)
# print(newUser.name)

# UsersCollection.insert_one(newUser.toDict())
    
class LoginManager:
    """
    Essa classe deve gerenciar os logins e a autenticação de sessões da aplicação
    """
    def __init__(self):
        self.tokenList = {} # "token":"_id"
        self.cacheLogged = {} # "_id" {"username": username, "name": name, "icon": icon}
        # self.tokenList = self.getSessionData

    def login(self, username, password):
        # Check if user exists
        user = UsersCollection.find_one({"username": username})
        if user:
            # Check the password
            if self.authenticate(user, password):
                # Generate a session token
                token = self.getToken()
                self.tokenList[token] = user["_id"]
                # SessionsCollection.insertOne({"token":token,"id":user["_id"]})
                return token
            else:
                print("ACCESS DENIED")
                return False
        else:
            print("Usuário inexistente")
            return False


    def authenticate(self, user, password):
        print(password)
        passMatches = bcrypt.checkpw(password.encode('utf-8'), user["password"])
        if passMatches:
            return True
        else:
            return False

    def validateToken(self, token, origin):
        #return bcrypt.checkpw(origin, token) Talvez isso resolva a linha abaixo
        return bcrypt.checkpw(origin, token)
    
    def getToken(self):
        return secrets.token_urlsafe(32)

    def isLogged(self, id):
        return id in list(self.tokenList.values())
    
    def isLoggedToken(self, token):
        return token in list(self.tokenList.keys())
    
    def getUserByToken(self, token):
        return self.tokenList[token]
    
    def updateCache(self, _id, username, name, icon):
        self.cacheLogged[_id] = {
            "username": username,
            "name": name,
            "icon": icon
        }
        
    


# def getSessionData():
#     sessionData = SessionsCollection.find()