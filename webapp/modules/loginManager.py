from utils import *
import bcrypt
import secrets

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
        return checkpw(origin, token)
    
    def getToken(self):
        return secrets.token_urlsafe(32)

    def isLogged(self, id):
        return id in list(self.tokenList.values())


# def getSessionData():
#     sessionData = SessionsCollection.find()