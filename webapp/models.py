from pymongo import MongoClient
import bcrypt
import secrets
from datetime import date, datetime
from .modules import TMDB, MediaModelPage, MediaModelSearch, QuickSort

# import webapp.modules as modules # Nossas classes estão aqui
# modules.DBElemensInterface.register(modules.User) # Registrando user como usuário da interface do db
# modules.DBElemensInterface.register(modules.Media) # mesma coisa com media

'''AVISO:
- Criei uma pasta modules e copiei todas as classes abaixo nela, além de classes que eu havia criado no outro repositório.
- Modificação feita por Nathan (19/11/24 - 10:00)'''

import os
from dotenv import load_dotenv
load_dotenv()
MONGODB_URI = os.getenv("URI") # URI pra conectar as parada

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

        
class Database:
    
    reviewTranslator = {
            "0":"undefined",
            "1":"Péssimo",
            "2":"Muito ruim",
            "3":"Ruim",
            "4":"Mediano",
            "5":"Bom",
            "6":"Muito bom",
            "7":"Perfeito"
        }
    
    @staticmethod
    def registerUser(user_obj):
        try:
            UsersCollection.insert_one(user_obj.toDict())
        
        except:
            return Database.insertionError()

    @staticmethod
    def registerMedia(media_obj):
        try:
            MediaCollection.insert_one(media_obj.toDict())
        
        except:
            return Database.insertionError()

    @staticmethod
    def registerReview(review_obj):
        try:
            ReviewsCollection.insert_one(review_obj.toDict())
        
        except:
            return Database.insertionError()
    
    @staticmethod
    def insertionError():
        print('Erro ao inserir objeto!\n')
        return False

    @staticmethod
    def getUserByID(id): # Returns User dictionary
        try:
            
            res = UsersCollection.find_one({'_id': id})
            return res
        
        except:
            print('Erro ao buscar usuário!')
            return False

    @staticmethod
    def getUserByUsername(username): # Returns User dictionary
        try:
            
            res = UsersCollection.find_one({'username': username})
            return res if res else None
        
        except:
            print('Erro ao buscar usuário!')
            return None

    @staticmethod
    def getAllUsers():
        try:
            res = list(UsersCollection.find())
            return res
        
        except:
            print('Erro ao buscar reviews!')
            return False

    @staticmethod
    def getMediaByID(id): # Returns Media dictionary
        try:
            
            res = MediaCollection.find_one({'_id': id})
            return res
        
        except:
            print('Erro ao buscar obra!')
            return False

    @staticmethod
    def getReviewByID(id):
        try:
            
            res = ReviewsCollection.find_one({'_id': id})
            return res
        
        except:
            print('Erro ao buscar Review!')
            return False

    @staticmethod
    def getAllReviews(): # return All Reviews
        try:
            res = list(ReviewsCollection.find())
            res = QuickSort(res, -1, "realDate").sorted
            return res
        
        except:
            print('Erro ao buscar reviews!')
            return False
        
    @staticmethod
    def getReviewsByAuthor(username): # return Media dictionary with review
        try:
            res = list(ReviewsCollection.find({"user_origin": username}))
            return res
        
        except:
            print('Erro ao buscar reviews!')
            return False

    @staticmethod
    def getReviewsByMedia(media_id): # return Media dictionary with review
        try:
            res = list(ReviewsCollection.find({"mediaTarget": media_id}))
            return res
        
        except:
            print('Erro ao buscar reviews!')
            return False
        
    @staticmethod
    def getReviewersByMedia(category, media_id):
        return list(UsersCollection.find({"watched.{}.{}".format(category, media_id): True}))
     
    @staticmethod
    def getReviewsToRenderHome(): # Return reviews in format "list of dict"
        temp = []
        reviews = Database.getAllReviews()
        users = Database.getAllUsers()
        medias = Database.getAllMedia()
        for review in reviews:
            for user in users:
                if user["username"] == review["user_origin"]:
                    for media in medias:
                        if media["_id"] == review["mediaTarget"]:
                            temp.append({
                                "icon": user["icon"],
                                "name": user["name"],
                                "username": user["username"],
                                "quality": review["content"]["review-quality"],
                                "qualityText": Database.reviewTranslator[review["content"]["review-quality"]] if review["content"]["review-quality"] else None,
                                "text": review["content"]["review-text"],
                                "target_name": media["name"],
                                "target_category": media["category"],
                                "target_api_id": media["api_id"],
                                "date": review["strDate"],
                                "realDate": review["realDate"],
                                "poster_path": media["posterPath"]
                            })
        return temp
    
    @staticmethod
    def getReviewsToRenderProfile(profile): # Return reviews in format "list of dict"
        username = profile["username"]
        watched = Database.getWatchedMedia(username)
        if not watched:
            return None
        reviews = Database.getReviewsByAuthor(username)
        if reviews:
            res = []
            # Buscar review
            for review in reviews:
                media_id = review["mediaTarget"]
                currentMedia = None
                # Buscar objeto de mídia
                for media in watched:
                    if media["_id"] == media_id:
                        currentMedia = media
                        break
                res.append({
                    "icon": profile["icon"],
                    "name": profile["name"],
                    "username": profile["username"],
                    "quality": review["content"]["review-quality"],
                    "qualityText": Database.reviewTranslator[review["content"]["review-quality"]] if review["content"]["review-quality"] else None,
                    "text": review["content"]["review-text"],
                    "target_name": currentMedia["name"],
                    "target_category": currentMedia["category"],
                    "target_api_id": currentMedia["api_id"],
                    "date": review["strDate"],
                    "realDate": review["realDate"]
                })
            res = QuickSort(res, -1, 'realDate').sorted
            return res
                
        else:
            return None
    
    @staticmethod
    def getReviewsToRenderMedia(category, media_id, username=None): # Return reviews in format "list of dict"
        res = {
            "selfReview": None,
            "otherReview": []
        }
        print(username)
        reviews = Database.getReviewsByMedia(media_id)
        if reviews:
            reviewers = Database.getReviewersByMedia(category, media_id)
            
            for review in reviews:
                # Para cada review
                currentAuthor = None
                for author in reviewers:
                    # Para cada usuário
                    if review["user_origin"] == author["username"]:
                        # Se usuário for o autor, currentAuthor recebe usuário
                        currentAuthor = author
                        if username and currentAuthor["username"] == username:
                            # Se o autor for o usuário do cliente
                            res["selfReview"] = {
                                "icon": currentAuthor["icon"],
                                "name": currentAuthor["name"],
                                "username": currentAuthor["username"],
                                "quality": review["content"]["review-quality"],
                                "qualityText": Database.reviewTranslator[review["content"]["review-quality"]] if review["content"]["review-quality"] else None,
                                "text": review["content"]["review-text"],
                                "date": review["strDate"],
                            }
                            # Define currentAuthor como None para que ele não seja adicionado ao otherReview
                            currentAuthor = None
                        # Rompe o laço ao achar o dono da review
                        break
                    # Continua o laço se não tiver encontrado o dono
                    continue
                if not currentAuthor:
                    continue
                res["otherReview"].append({
                    "icon": currentAuthor["icon"],
                    "name": currentAuthor["name"],
                    "username": currentAuthor["username"],
                    "quality": review["content"]["review-quality"],
                    "qualityText": Database.reviewTranslator[review["content"]["review-quality"]] if review["content"]["review-quality"] else None,
                    "text": review["content"]["review-text"],
                    "date": review["strDate"],
                    "realDate": review["realDate"]
                })
        
            res["otherReview"] = QuickSort(res["otherReview"], -1, 'realDate').sorted
            print(res)
            return res
            
        else:
            return None
        
    @staticmethod
    def getAllMedia():
        try:
            res = list(MediaCollection.find())
            return res
        
        except:
            print('Erro ao buscar reviews!')
            return False
     
    @staticmethod   
    def getWatchedMedia(username):
        res = list(MediaCollection.find({"viewsList": {"$all": [username]}}))
        return res if res else None
    
    @staticmethod
    def getFollowersOf(username):
        res = list(UsersCollection.find({"following": {"$all": [username]}}))
        return res
    
    @staticmethod
    def getWhoUserIsFollowing(username):
        res = list(UsersCollection.find({"followers": {"$all": [username]}}))
        return res
    
    @staticmethod
    def getFollowInfo(username):
        followInfo = {
            "followers": [],
            "following": []
        }
        followingList = Database.getWhoUserIsFollowing(username)
        for user in followingList:
            followInfo["following"].append({
                "name": user["name"],
                "username": user["username"],
                "icon": user["icon"]
            })
        followerList = Database.getFollowersOf(username)
        for user in followerList:
            followInfo["followers"].append({
                "name": user["name"],
                "username": user["username"],
                "icon": user["icon"]
            })
        return followInfo
    
    @staticmethod
    def getProfileDiary(profile):
        res = QuickSort(profile["diary"], -1, 'realDate').sorted if profile["diary"] else None
        return res
    
    @staticmethod
    def searchMediaByQuery(category, query):
        queryResult = []
        if category == "movie":
            temp = TMDB.search("movie", query)
            for result in temp:
                queryResult.append(
                    MediaModelSearch.build(
                        "movie",
                        result["id"],
                        result["title"],
                        result["overview"],
                        "https://image.tmdb.org/t/p/w300_and_h450_bestv2{}".format(result["poster_path"]) if result["poster_path"] else None,
                        result["vote_average"],
                        str(result["release_date"])[0:4:1]
                    )
                )
        elif category == "serie":
            temp = TMDB.search("tv", query)
            for result in temp:
                print(result["origin_country"])
                if result["origin_country"] == [] or result["origin_country"][0] == "JP": continue
                queryResult.append(
                    MediaModelSearch.build(
                        "serie",
                        result["id"],
                        result["name"],
                        result["overview"],
                        "https://image.tmdb.org/t/p/w300_and_h450_bestv2{}".format(result["poster_path"]) if result["poster_path"] else None,
                        result["vote_average"],
                        str(result["first_air_date"])[0:4:1]
                    )
                )
        elif category == "anime":
            temp = TMDB.search("tv", query)
            for result in temp:
                if result["origin_country"] == [] or result["origin_country"][0] != "JP": continue
                queryResult.append(
                    MediaModelSearch.build(
                        "anime",
                        result["id"],
                        result["name"],
                        result["overview"],
                        "https://image.tmdb.org/t/p/w300_and_h450_bestv2{}".format(result["poster_path"]) if result["poster_path"] else None,
                        result["vote_average"],
                        str(result["first_air_date"])[0:4:1]
                    )
                )
        elif category == "game":
            pass
        elif category == "book":
            pass
        elif category == "user":
            pass
        else:
            print("Erro na categoria da requisição")
            return
        return queryResult
    
    @staticmethod
    def searchSingleMedia(category, id):
        if category == "movie":
            mediaObj = TMDB.getByID("movie", id)
            temp_size = str(mediaObj["runtime"]) + 'm' if mediaObj["runtime"] < 60 else (str(mediaObj["runtime"]//60) + 'h' + str(mediaObj["runtime"]%60) + 'm')
            print(mediaObj)
            mediaObj = MediaModelPage.build(
                        "movie",
                        mediaObj["id"],
                        mediaObj["title"],
                        mediaObj["overview"],
                        "https://image.tmdb.org/t/p/w300_and_h450_bestv2{}".format(mediaObj["poster_path"]) if mediaObj["poster_path"] else None,
                        mediaObj["vote_average"],
                        str(mediaObj["release_date"])[0:4:1],
                        "https://image.tmdb.org/t/p/w1920_and_h1080_bestv2{}".format(mediaObj["backdrop_path"]) if mediaObj["backdrop_path"] else None,
                        mediaObj["genres"],
                        {
                            "time": temp_size
                        }
                    )
        elif category == "serie":
            mediaObj = TMDB.getByID("tv", id)
            temp_episode = 0
            for season in mediaObj["seasons"]:
                temp_episode += season["episode_count"]
            mediaObj = MediaModelPage.build(
                        "serie",
                        mediaObj["id"],
                        mediaObj["name"],
                        mediaObj["overview"],
                        "https://image.tmdb.org/t/p/w300_and_h450_bestv2{}".format(mediaObj["poster_path"]) if mediaObj["poster_path"] else None,
                        mediaObj["vote_average"],
                        str(mediaObj["first_air_date"])[0:4:1],
                        "https://image.tmdb.org/t/p/w1920_and_h1080_bestv2{}".format(mediaObj["backdrop_path"]) if mediaObj["backdrop_path"] else None,
                        mediaObj["genres"],
                        {
                            "seasons": len(mediaObj["seasons"]),
                            "episode_count": temp_episode
                        },
                    )
        elif category == "anime":
            mediaObj = TMDB.getByID("tv", id)
            temp_episode = 0
            for season in mediaObj["seasons"]:
                temp_episode += season["episode_count"]
            mediaObj = MediaModelPage.build(
                        "anime",
                        mediaObj["id"],
                        mediaObj["name"],
                        mediaObj["overview"],
                        "https://image.tmdb.org/t/p/w300_and_h450_bestv2{}".format(mediaObj["poster_path"]) if mediaObj["poster_path"] else None,
                        mediaObj["vote_average"],
                        str(mediaObj["first_air_date"])[0:4:1],
                        "https://image.tmdb.org/t/p/w1920_and_h1080_bestv2{}".format(mediaObj["backdrop_path"]) if mediaObj["backdrop_path"] else None,
                        mediaObj["genres"],
                        {
                            "seasons": len(mediaObj["seasons"]),
                            "episode_count": temp_episode
                        }
                        ,
                    )
        elif category == "game":
            pass
        elif category == "book":
            pass
        else:
            print("Erro na categoria da requisição")
            return
        return mediaObj
    
    @staticmethod
    def editReview(reviewObj):
        try:
            id = reviewObj["_id"]
            ReviewsCollection.replace_one({"_id": id}, reviewObj)
        except:
            print("Erro na edição re review")
            return None
    
    @staticmethod
    def deleteReview(review):
        id = review["_id"]
        try:
            ReviewsCollection.delete_one({"_id": id})
        except:
            print("Erro na deleção de review")
            return None
        
    @staticmethod
    def deleteReviewByID(id):
        try:
            ReviewsCollection.delete_one({"_id": id})
        except:
            print("Erro na deleção de review")
            return None
    
    @staticmethod
    def refreshUser(user):
        """
        Recebe dicionário de usuário e atualiza o equivalente no banco
        """
        id = user["_id"]
        try:
            UsersCollection.replace_one({"_id": id}, user)
        except:
            print("Erro na atualização de perfil")
            return None
    
    @staticmethod
    def refreshMedia(media):
        id = media["_id"]
        try:
            MediaCollection.replace_one({"_id": id}, media)
        except:
            print("Erro na atualização de mídia")
            return None
    
    
    
    