from webapp.models import UsersCollection, LoginManager
import bcrypt

# simulando login 

# temp = UsersCollection.find_one({"username": "seila"}) # pegando usuario do banco

# if temp :
        
#     print(temp)

#     res = bcrypt.checkpw('abacate'.encode('utf-8'), temp["password"]) # senha certa

#     print(res)

#     res = bcrypt.checkpw('mamão'.encode('utf-8'), temp["password"]) # senha errada

#     print(res)

#     print(temp["_id"])

# else:
#     print("Esse cara n existe")


# print(key)


logins = LoginManager()

# logins.login("seila", "abacate")
logins.login("seila", "aabacate")

print(logins.tokenList)