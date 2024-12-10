from pymongo import MongoClient
import bcrypt
import secrets
from datetime import date, datetime
from typing import Type
from .modules import TMDB, MediaModelSearch, QuickSort, AnimeModelPage, SerieModelPage, MovieModelPage, AnimeModelSearch, SerieModelSearch, MovieModelSearch, IGDB, GameModelSearch, GameModelPage, DBElementsAbstract, GoogleBooks, BookModelPage, BookModelSearch

# import webapp.modules as modules # Nossas classes estão aqui
# modules.DBElemensInterface.register(modules.User) # Registrando user como usuário da interface do db
# modules.DBElemensInterface.register(modules.Media) # mesma coisa com media

'''AVISO:
- Criei uma pasta modules e copiei todas as classes abaixo nela, além de classes que eu havia criado no outro repositório.
- Modificação feita por Nathan (19/11/24 - 10:00)'''

import os
from dotenv import load_dotenv
load_dotenv()
MONGODB_URI:str = os.getenv("URI") # URI pra conectar as parada

# Mongo Client
client: Type[MongoClient] = MongoClient(MONGODB_URI) # Cria o client q consegue fazer o crud

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
    
    reviewTranslator:dict = {
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
    def registerUser(user_obj:Type[DBElementsAbstract]):
        """
        Função: Registrar usuário no banco de dados
        Recebe: Objeto da classe User
        Retorna: None
        """
        try:
            UsersCollection.insert_one(user_obj.toDict())
            return None
        
        except:
            return Database.insertionError()

    @staticmethod
    def registerMedia(media_obj:Type[DBElementsAbstract]):
        """
        Função: Registrar mídia no banco de dados
        Recebe: Objeto da classe Media
        Retorna: None
        """
        try:
            MediaCollection.insert_one(media_obj.toDict())
            return None
        
        except:
            return Database.insertionError()

    @staticmethod
    def registerReview(review_obj:Type[DBElementsAbstract]):
        """
        Função: Registrar review no banco de dados
        Recebe: Objeto da classe Review
        Retorna: None
        """
        try:
            ReviewsCollection.insert_one(review_obj.toDict())
        
        except:
            return Database.insertionError()
    
    @staticmethod
    def insertionError():
        """
        Função: Retornar erro de inserção no terminal
        Retorna: False
        """
        print('Erro ao inserir objeto!\n')
        return False

    @staticmethod
    def getUserByID(id:any): # Returns User dictionary
        """
        Função: Recuperar um usuário do banco usando o ID
        Recebe: ID do usuário no banco
        Retorna: Dicionário de usuário (Equivalente à User.toDict())
        """
        try:
            
            res:dict = UsersCollection.find_one({'_id': id})
            return res
        
        except:
            print('Erro ao buscar usuário!')
            return False

    @staticmethod
    def getUserByUsername(username:str): # Returns User dictionary
        """
        Função: Recuperar um usuário do banco usando o username
        Recebe: username do usuário no banco
        Retorna: Dicionário de usuário (Equivalente à User.toDict())
        """
        try:
            
            res:dict = UsersCollection.find_one({'username': username})
            return res if res else None
        
        except:
            print('Erro ao buscar usuário!')
            return None

    @staticmethod
    def getAllUsers():
        """
        Função: Recupera todos os usuários do banco
        Retorna: Lista de dicionários de usuário (Equivalente à uma lista de User.toDict())
        """
        try:
            res:list = list(UsersCollection.find())
            return res
        
        except:
            print('Erro ao buscar reviews!')
            return False

    @staticmethod
    def getMediaByID(id:str): # Returns Media dictionary
        """
        Função: Recuperar uma mídia do banco usando o ID
        Recebe: ID da mídia no banco (no formato <category>_<api_id>)
        Retorna: Dicionário de mídia (Equivalente à Media.toDict())
        """
        try:
            
            res:dict = MediaCollection.find_one({'_id': id})
            return res
        
        except:
            print('Erro ao buscar obra!')
            return False

    @staticmethod
    def getReviewByID(id:str):
        """
        Função: Recuperar uma review do banco usando o ID
        Recebe: ID da review no banco (no formato <origin_user>_<category>_<api_id>)
        Retorna: Dicionário de review (Equivalente à Review.toDict())
        """
        try:
            
            res:dict = ReviewsCollection.find_one({'_id': id})
            return res
        
        except:
            print('Erro ao buscar Review!')
            return False

    @staticmethod
    def getAllReviews(): # return All Reviews
        """
        Função: Recupera todas as reviews do banco
        Retorna: Lista de dicionários de review (Equivalente à uma lista de Review.toDict())
        """
        try:
            res:list = list(ReviewsCollection.find())
            res = QuickSort(res, -1, "realDate").sorted
            return res
        
        except:
            print('Erro ao buscar reviews!')
            return False
        
    @staticmethod
    def getReviewsByAuthor(username:str): # return Media dictionary with review
        """
        Função: Recuperar todas as reviews feitas por um determinado usuário
        Recebe: username do usuário alvo
        Retorna: Lista de dicionátios de review (Equivalente à uma lista de Review.toDict())
        """
        try:
            res:list = list(ReviewsCollection.find({"user_origin": username}))
            return res
        
        except:
            print('Erro ao buscar reviews!')
            return False

    @staticmethod
    def getReviewsByMedia(media_id:str): # return Media dictionary with review
        """
        Função: Recuperar todas as reviews de uma determinada obra
        Recebe: ID da mídia no banco (no formato <category>_<api_id>)
        Retorna: Lista de dicionários de review (Equivalente à uma lista de Review.toDict())
        """
        try:
            res:list = list(ReviewsCollection.find({"mediaTarget": media_id}))
            return res
        
        except:
            print('Erro ao buscar reviews!')
            return False
        
    @staticmethod
    def getReviewersByMedia(category:str, media_id:str):
        """
        Função: Recuperar todos os usuários que avaliaram uma obra
        Recebe: Categoria da obra no BANCO e ID da obra na API.
        Retorna: Lista de dicionários de usuário (Equivalente à uma lista de User.toDict())
        """
        # ? Quando um usuário marca uma obra como vista, é acrescentada a chave equivalente ao ID da obra (<category>_<api_id>). Essa chave aponta para "False" se a obra foi apenas vista e "True" se a obra foi vista e avaliada.
        return list(UsersCollection.find({"watched.{}.{}".format(category, media_id): True})) 
     
    @staticmethod
    def getReviewsToRenderHome(): # Return reviews in format "list of dict"
        """
        Função: Gerar uma lista de reviews com as informações necessárias para renderizar a Home page.
        Retorna: Lista de dicionários de review em um formato único que une informações de usuário, mídia e review.
        """
        temp:list = []
        reviews:list = Database.getAllReviews()
        users:list = Database.getAllUsers()
        medias:list = Database.getAllMedia()
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
    def getReviewsToRenderProfile(profile:dict): # Return reviews in format "list of dict"
        """
        Função: Gerar uma lista de reviews com as informações necessárias para renderizar o perfil de um usuário.
        Recebe: Dicionário de usuário (Equivalente à User.toDict())
        Retorna: Lista de dicionários de review em um formato único que une informações do dono do perfil, mídia e review.
        """
        username:str = profile["username"]
        watched:list = Database.getWatchedMedia(username)
        if not watched:
            return None
        reviews:list = Database.getReviewsByAuthor(username)
        if reviews:
            res:list = []
            # Buscar review
            for review in reviews:
                media_id:str = review["mediaTarget"]
                currentMedia:dict = None
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
    def getReviewsToRenderMedia(category:str, media_id:str, username:str=None): # Return reviews in format "list of dict"
        """
        Função: Gerar uma lista de reviews com as informações necessárias para renderizar a página de uma mídia.
        Recebe: Categoria no BANCO, ID da API e opcionalmente recebe o username do cliente se estiver logado para saber diferenciar as reviews dele das ademais
        Retorna: Lista de dicionários de review em um formato único que une informações da review, mídia e autor da review.
        """
        res:dict = {
            "selfReview": None,
            "otherReview": []
        }
        reviews:list = Database.getReviewsByMedia(media_id)
        if reviews:
            reviewers:list = Database.getReviewersByMedia(category, media_id)
            
            for review in reviews:
                # Para cada review
                currentAuthor:dict = None
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
            if res["otherReview"]:
                res["otherReview"] = QuickSort(res["otherReview"], -1, 'realDate').sorted
            return res
            
        else:
            return None
        
    @staticmethod
    def getAllMedia():
        """
        Função: Recuperar todas as mídias do banco.
        Retorna: Lista de dicionários de mídia (Equivalente á uma lista de Media.toDict()).
        """
        try:
            res:list = list(MediaCollection.find())
            return res
        
        except:
            print('Erro ao buscar reviews!')
            return False
     
    @staticmethod   
    def getWatchedMedia(username:str):
        """
        Função: Recuperar todas as mídias vistas por um usuário.
        Recebe: username do usuário alvo
        Retorna: Lista de dicionários de mídia (Equivalente á uma lista de Media.toDict()).
        """
        res:list = list(MediaCollection.find({"viewsList": {"$all": [username]}}))
        return res if res else None
    
    @staticmethod
    def getFollowersOf(username:str):
        """
        Função: Recuperar todos os seguidores de um usuário.
        Recebe: username do usuário alvo
        Retorna: Lista de dicionários de usuário (Equivalente á uma lista de User.toDict()).
        """
        res:list = list(UsersCollection.find({"following": {"$all": [username]}}))
        return res
    
    @staticmethod
    def getWhoUserIsFollowing(username:str):
        """
        Função: Recuperar todos os usuários que um usuário alvo segue.
        Recebe: username do usuário alvo
        Retorna: Lista de dicionários de usuário (Equivalente á uma lista de User.toDict()).
        """
        res:list = list(UsersCollection.find({"followers": {"$all": [username]}}))
        return res
    
    @staticmethod
    def getFollowInfo(username:str):
        """
        Função: Recuperar as informações de followers e following de um usuário alvo.
        Recebe: username do usuário alvo
        Retorna: Dicionário com uma lista de followers e uma de following.
        """
        followInfo:dict = {
            "followers": [],
            "following": []
        }
        followingList:list = Database.getWhoUserIsFollowing(username)
        for user in followingList:
            followInfo["following"].append({
                "name": user["name"],
                "username": user["username"],
                "icon": user["icon"]
            })
        followerList:list = Database.getFollowersOf(username)
        for user in followerList:
            followInfo["followers"].append({
                "name": user["name"],
                "username": user["username"],
                "icon": user["icon"]
            })
        return followInfo
    
    @staticmethod
    def getProfileDiary(profile:dict):
        """
        Função: Recuperar o diário de um usuário na ordem cronológica correta.
        Recebe: dicionário de usuário (Equivalente á User.toDict())
        Retorna: Lista de dicionários equivalentes á páginas do diário.
        """
        res = QuickSort(profile["diary"], -1, 'realDate').sorted if profile["diary"] else None
        return res
    
    @staticmethod
    def searchMediaByQuery(category:str, query:str):
        """
        Função: Realizar uma busca por uma obra em sua respectiva API.
        Recebe: Categoria (que vai revelar a API que deve ser usada) e a query da busca.
        Retorna: Lista de dicionários onde cada dicionário corresponde á uma obra, com suas informações necessárias para renderizar a página de busca.
        """
        queryResult:list = []
        if category == "movie":
            temp:list = TMDB.search("movie", query)
            for result in temp:
                queryResult.append(
                    MovieModelSearch(result).build()
                )
        elif category == "serie":
            temp:list = TMDB.search("tv", query)
            for result in temp:
                if result["origin_country"] == [] or result["origin_country"][0] == "JP": continue
                queryResult.append(
                    SerieModelSearch(result).build()
                )
        elif category == "anime":
            temp:list = TMDB.search("tv", query)
            for result in temp:
                if result["origin_country"] == [] or result["origin_country"][0] != "JP": continue
                queryResult.append(
                    AnimeModelSearch(result).build()
                )
        elif category == "game":
            temp:list = IGDB.search(query)
            for result in temp:
                queryResult.append(
                    GameModelSearch(result).build()
                )
        elif category == "book":
            temp:list = GoogleBooks.search(query)
            for result in temp:
                queryResult.append(
                    BookModelSearch(result).build()
                )
        elif category == "user":
            pass
        else:
            print("Erro na categoria da requisição")
            return
        return queryResult
    
    @staticmethod
    def searchSingleMedia(category:str, id:str):
        """
        Função: Recuperar informações de uma mídia específica.
        Recebe: categoria da obra e ID dela na API
        Retorna: Dicionário com as informações da obra (Equivalente á MediaModelPage.build(), que faz justamente esse trabalho de estruturar as informações).
        """
        if not id:
            print("Erro no identificador da requisição")
            return
        if category == "movie":
            mediaObj:dict = TMDB.getByID("movie", id)
            mediaObj = MovieModelPage(mediaObj)
        elif category == "serie":
            mediaObj:dict = TMDB.getByID("tv", id)
            mediaObj = SerieModelPage(mediaObj)
        elif category == "anime":
            mediaObj:dict = TMDB.getByID("tv", id)
            mediaObj = AnimeModelPage(mediaObj)
        elif category == "game":
            mediaObj:dict = IGDB.getByID(id)
            mediaObj = GameModelPage(mediaObj)
        elif category == "book":
            mediaObj:dict = GoogleBooks.getByID(id)
            mediaObj = BookModelPage(mediaObj)
        else:
            print("Erro na categoria da requisição")
            return
        return mediaObj.build()
    
    @staticmethod
    def editReview(reviewObj:dict):
        """
        Função: Editar uma review no banco.
        Recebe: dicionário de review (Equivalente á Review.toDict())
        Retorna: None.
        """
        try:
            id:str = reviewObj["_id"]
            ReviewsCollection.replace_one({"_id": id}, reviewObj)
            return None
        except:
            print("Erro na edição re review")
            return None
    
    @staticmethod
    def deleteReview(review:dict):
        """
        Função: Deletar review do banco de dados.
        Recebe: dicionário da review (Equivalente á Review.toDict())
        Retorna: None.
        """
        id:str = review["_id"]
        try:
            ReviewsCollection.delete_one({"_id": id})
            return None
        except:
            print("Erro na deleção de review")
            return None
        
    @staticmethod
    def deleteReviewByID(id:str):
        """
        Função: Deletar review do banco usando o ID dela.
        Recebe: ID da review no banco (no formato <user_origin>_<category>_<api_id>)
        Retorna: None.
        """
        try:
            ReviewsCollection.delete_one({"_id": id})
        except:
            print("Erro na deleção de review")
            return None
    
    @staticmethod
    def refreshUser(user:dict):
        """
        Função: Atualizar usuário no banco.
        Recebe: dicionário de usuário (Equivalente á User.toDict())
        Retorna: None.
        """
        id:str = user["_id"]
        try:
            UsersCollection.replace_one({"_id": id}, user)
            return None
        except:
            print("Erro na atualização de perfil")
            return None
    
    @staticmethod
    def refreshMedia(media:dict):
        """
        Função: Atualizar mídia no banco.
        Recebe: dicionário de mídia (Equivalente á Media.toDict())
        Retorna: None.
        """
        id:str = media["_id"]
        try:
            MediaCollection.replace_one({"_id": id}, media)
            return None
        except:
            print("Erro na atualização de mídia")
            return None
    
    
    
    