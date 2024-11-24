from pymongo import MongoClient
import bcrypt
import secrets

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
    
    def __init__(self, name, username, email, password, icon=0, banner=0, bio='', followers=[], following=[], watched={}, watchList={}, reviews=[], config={}):
        self.name = name # Nome qualquer
        self.username = username # Nome de usuário (único)
        self.icon = icon # Código do ícone
        self.banner = banner # Código do banner
        self.bio = bio # Bio (até 200 char)
        self.email = email # Email
        self.password =  self.hashpw(password)# Senha...
        self.followers = followers # Quem segue ele (lista de ids)
        self.following = following # Quem ele segue (lista de ids)
        self.watched = watched # Mídias que ele já assistiu, em ordem de preferência
        self.watchList = watchList # Mídias que pretende consumir // está assistindo {estado: pretende assistir | assistindo}
        self.reviews = reviews # Lista com códigos das reviews do usuário
        self.config = config # Configurações de personalização do usuário
        
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
            "following": self.following,
            "watched": self.watched,
            "watchList": self.watchList,
            "reviews": self.reviews,
            "config": self.config
        }

    def hashpw(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
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
        self.reviews = reviews # {"owner_id": review_object ou review_id}
        
    def toDict(self):
        """Converte a obra pra um dicionário (pra poder colocar no db 😉)"""

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
        return checkpw(origin, token)
    
    def getToken(self):
        return secrets.token_urlsafe(32)

    def isLogged(self, id):
        return id in list(self.tokenList.values())


# def getSessionData():
#     sessionData = SessionsCollection.find()