import bcrypt
import secrets
from webapp.models import Database
from django.http import HttpRequest
from typing import Type

class LoginCache:
    def __init__(self, username:str, name:str, icon:str):
        self.username = username
        self.name = name
        self.icon = icon
        
    def toDict(self):
        return {
            "username": self.username,
            "name": self.name,
            "icon": self.icon
        }


class LoginManager:
    """
    Essa classe deve gerenciar os logins e a autenticação de sessões da aplicação
    """
    def __init__(self):
        self.tokenList:dict = {} # "token":"_id"
        self.cacheLogged:dict = {} # "_id":LoginCache {"username": username, "name": name, "icon": icon}
        # self.tokenList = self.getSessionData

    def login(self, username:str, password:str):
        # Check if user exists
        user:dict = Database.getUserByUsername(username)
        if user:
            # Check the password
            if self.authenticate(user, password):
                # Generate a session token
                token:str = self.getToken()
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
        passMatches:bool = bcrypt.checkpw(password.encode('utf-8'), user["password"])
        if passMatches:
            return True
        else:
            return False

    def validateToken(self, token:bytes, origin:bytes):
        #return bcrypt.checkpw(origin, token) Talvez isso resolva a linha abaixo
        return bcrypt.checkpw(origin, token)
    
    def getToken(self):
        return secrets.token_urlsafe(32)

    def isLogged(self, id):
        return id in list(self.tokenList.values())
    
    def isLoggedToken(self, token:str):
        return token in list(self.tokenList.keys())
    
    def getUserByToken(self, token:str):
        return self.tokenList[token]
    
    def cache(self, _id, username:str, name:str, icon:str):
        self.cacheLogged[_id] = LoginCache(username, name, icon)
    
    def updateCache(self, _id, username:str, name:str, icon:str):
        if _id in self.cacheLogged:
            self.cache(_id, username, name, icon)
        else:
            print("Current login is not cached")
            return None
        
        
    def isLoggedRequest(self, request:Type[HttpRequest]):
        accessToken:str = request.COOKIES.get('sessionToken')
        if not accessToken:
            return False
        if self.isLoggedToken(accessToken):
            return True
        else:
            return False
        
    def getUserByRequest(self, request:Type[HttpRequest]):
        """
        Recebe requisição do usuário
        
        Retorna ID do usuário se estiver logado ou None se não estiver
        """
        if self.isLoggedRequest(request):
            accessToken:str = request.COOKIES.get('sessionToken')
            return self.getUserByToken(accessToken)
        return None
        
    def recoverCached(self, _id):
        if not self.isLogged(_id):
            return None
        return self.cacheLogged[_id].toDict() if self.cacheLogged[_id] else None
    
    def recoverCachedByRequest(self, request:Type[HttpRequest]):
        if self.isLoggedRequest(request):
            id = self.getUserByRequest(request)
            return self.recoverCached(id)
        else:
            return None
        
    def deleteLoginByCache(self, id):
        if self.isLogged(id):
            self.cacheLogged.pop(id)
        else:
            print("Cache de login inexistente")