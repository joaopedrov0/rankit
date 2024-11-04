from pymongo import MongoClient
import bcrypt

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
    
    def __init__(self, name, username, email, password, icon=0, banner=0, bio='', followers=[], following=[], watched=[], watchList=[], reviews=[], config={}):
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
            "reviews": self.reviews
        }

    def hashpw(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
# newUser = User("RainanKaneka", "rainankaneka", "4", "0", "sim", "email.rainan@gmail.com", "12345")

# print(newUser)
# print(newUser.name)

# UsersCollection.insert_one(newUser.toDict())
    
class LoginManager:
    """
    Essa classe deve gerenciar os logins e a autenticação de sessões da aplicação
    """
    def __init__():
        tokenList = {} # "token":"_id"

    def login(self):
        pass

    def authenticate(self, username, password):
        user = UsersCollection.find_one({"username": username})
        if user:
            passMatches = bcrypt.checkpw(password.encode('utf-8'), user["password"])
            if passMatches:
                return True
            else:
                return False
        else:
            print("Usuário inexistente")
            return False

