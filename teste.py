from webapp.models import UsersCollection, LoginManager, User

UsersCollection.insert_one(User("RainanKaneka", "rainankaneka", "", "bazinga", 4, 6, "A dream, i saw a dream, a dream that wouldn't end, over and over i repeated and corrected every mistake, but before i knew it, i lost count, i died, over one hundred million times.").toDict())

# a = UsersCollection.replace_one({"username": "rainankaneka"}, {"reviews": {
#     "movie": [],
#     "serie": [],
#     "anime": [],
#     "game": [],
#     "book": []
# }})


# print(a)


# import bcrypt

# print(bcrypt)

# # simulando login 

# # temp = UsersCollection.find_one({"username": "seila"}) # pegando usuario do banco

# # if temp :
        
# #     print(temp)

# #     res = bcrypt.checkpw('abacate'.encode('utf-8'), temp["password"]) # senha certa

# #     print(res)

# #     res = bcrypt.checkpw('mamão'.encode('utf-8'), temp["password"]) # senha errada

# #     print(res)

# #     print(temp["_id"])

# # else:
# #     print("Esse cara n existe")


# # print(key)


# logins = LoginManager()

# # logins.login("seila", "abacate")
# logins.login("seila", "aabacate")

# print(logins.tokenList)


# UsersCollection.replace_many(True, {"watched": {}})