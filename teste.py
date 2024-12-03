from webapp.models import UsersCollection, LoginManager, User, Review, MediaCollection


# review = Review("rainankaneka", "anime", 92382)
# print(review)
# print(review.toDict())


# cursor = UsersCollection.find({
#     # "watched": {
#     #     "anime":{
#     #         "anime_209867": True
#     #     }
#     # }
#     "watched.anime.anime_209867": True
# })
# for doc in cursor:
#     print(doc)

watchedMedia = list(MediaCollection.find({"viewsList": {"$all": ["rainankaneka"]}}))
print(watchedMedia)
# UsersCollection.insert_one(User("RainanKaneka", "rainankaneka", "", "bazinga", 4, 6, "A dream, i saw a dream, a dream that wouldn't end, over and over i repeated and corrected every mistake, but before i knew it, i lost count, i died, over one hundred million times.").toDict())

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


# {
#     "watched":{
#         "anime":{
#             "universalMediaId": None | "reviewId"
#             },
#         "movie":{},
#         "serie":{}
#     }
# }