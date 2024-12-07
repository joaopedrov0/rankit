from webapp.models import UsersCollection, LoginManager, User, Review, MediaCollection, ReviewsCollection

from webapp.modules import QuickSort, RawgGames

from datetime import date, datetime




print(RawgGames.search("Outer wilds"))















# print(home_fs.listdir('/'))
# review = Review("rainankaneka", "anime", 92382)
# print(review)
# print(review.toDict())






# allUsers = list(ReviewsCollection.find())
# for user in allUsers:
#     user["realDate"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     user["strDate"] = date.today().strftime("%d/%m/%Y")
#     ReviewsCollection.replace_one({"_id": user["_id"]}, user)
    
# allUsers = list(UsersCollection.find())
# for user in allUsers:
#     # anime = list(user["watched"]["anime"].keys())
#     # movie = list(user["watched"]["movie"].keys())
#     # serie = list(user["watched"]["serie"].keys())
#     # temp = [*anime, *movie, *serie]
#     # for page in temp:
#     #     user["diary"].append({
#     #         "media_id": page,
#     #         "realDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#     #         "strDate": date.today().strftime("%d/%m/%Y")
#     #     })
#     # print(temp)
#     diary = QuickSort(user["diary"], -1, 'realDate').sorted
        
#     watchedMedia = list(MediaCollection.find({"viewsList": {"$all": [user["username"]]}}))
    
    
#     for page in diary:
#         currentPage = page["media_id"]
        
#         for media in watchedMedia:
#             if currentPage == media["_id"]:
#                 page["name"] = media["name"]
#                 page["api_id"] = media["api_id"]
#                 page["category"] = media["category"]
#                 page["banner_path"] = media["bannerPath"]
    
#     # user["watchedNumber"] = len(user["diary"])
    
#     user["diary"] = diary
    
#     UsersCollection.replace_one({"_id": user["_id"]}, user)
    
# allUsers = list(MediaCollection.find())
# for user in allUsers:
#     user["realDate"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     user["strDate"] = date.today().strftime("%d/%m/%Y")
#     MediaCollection.replace_one({"_id": user["_id"]}, user)







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

# watchedMedia = list(MediaCollection.find({"viewsList": {"$all": ["rainankaneka"]}}))
# print(watchedMedia)
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