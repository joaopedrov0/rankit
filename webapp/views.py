from django.shortcuts import render, redirect
from .models import Database
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotModified, JsonResponse, HttpRequest
from .modules import User, Media, Review, DatabaseCRUDInterface, DatabaseRenderInterface
from datetime import datetime, date
from .modules.loginManager import LoginManager

from typing import Type

DatabaseCRUDInterface.register(Database)
DatabaseRenderInterface.register(Database)

# Recuperando icons e banners
import os
from fs import open_fs
fs_manager = open_fs(os.path.join(os.path.dirname(__file__), "..", "templates", "static", "img"))
ICONS_LIST = fs_manager.listdir('/icon')
BANNER_LIST = fs_manager.listdir('/banner')


LOGIN_MANAGER = LoginManager()

def home(request: Type[HttpRequest]):
    
    reviews:list = Database.getReviewsToRenderHome()
    
    if LOGIN_MANAGER.isLoggedRequest(request): # Se estiver logado
        userID = LOGIN_MANAGER.getUserByRequest(request)
        user = Database.getUserByID(userID)
        return render(request, 'home.html', {"logged":True, "user": user, "reviews": reviews})
    else: # Se não estiver logado
        return render(request, 'home.html', {"logged":False, "reviews": reviews})

def profile(request: Type[HttpRequest], username: str):
    
    currentProfile:dict = Database.getUserByUsername(username) # Recupera o perfil atual
    
    logged:bool = False # Verificar se cliente está logado
    selfProfile:bool = False # Verificar se o cliente está no próprio perfil
    following:bool = False # Verificar se o cliente segue o perfil alvo
    clientProfile:dict = None # Perfil do cliente
    
    if LOGIN_MANAGER.isLoggedRequest(request): # Se o cliente estiver logado
        logged = True
        
        clientID = LOGIN_MANAGER.getUserByRequest(request)
        
        selfProfile = True if currentProfile["_id"] == clientID else False
        
        clientProfile = LOGIN_MANAGER.recoverCached(clientID)
        
        if selfProfile:
            following = False
        else:
            if clientProfile["username"] in currentProfile["followers"]:
                following = True

    if currentProfile:
        # Se o perfil existir, gera as informações de seguidores, diário e reviews
        
        # Gerando informações de seguidores
        followInfo:dict = Database.getFollowInfo(username)
        
        # Gerando diário
        diary:dict = Database.getProfileDiary(currentProfile)
        
        # Gerando reviews para renderizar
        reviews:list = Database.getReviewsToRenderProfile(currentProfile)
        
        return render(request, 'profile.html', {
            "currentProfile": currentProfile, 
            "logged": logged, 
            "selfProfile": selfProfile, 
            "reviews": reviews, 
            "diary": diary, 
            "following": following, 
            "followInfo": followInfo,
            "clientProfile": clientProfile
            })

    else:
        # Se o perfil não existir, direciona pra página "not-found".
        return render(request, 'not-found.html')

@csrf_exempt
def cadastro(request: Type[HttpRequest]):
    
    # Se for requisição GET ele retorna a página, se for POST ele reconhece como uma resposta de formulário
        
    if request.method == 'GET': 
        
        return render(request, 'cadastro.html')
    
    elif request.method == 'POST':
        username:str = request.POST.get('username')
        
        if Database.getUserByUsername(username) == None:
            # Se não existir um usuário com esse username
            
            name:str = request.POST.get('name').strip()
            username = request.POST.get('username').strip()
            email:str = request.POST.get('email')
            password:str = request.POST.get('password')
            password_confirm:str = request.POST.get('confirm-password')
            
            if password != password_confirm:
                return render(request, 'cadastro.html', {"unmatchpassword": True})
            
            if name and username and email and password:
                # Se todos os campos estiverem preenchidos
                
                newUser:Type[User] = User(
                    name,
                    username,
                    email,
                    password
                )
                
                Database.registerUser(newUser)
                
            else:
                # Se faltar campos para preencher
                
                return render(request, 'cadastro.html', {"missing": True})
                
        else:
            # Se o username já estiver sendo usado
            
            return render(request, 'cadastro.html', {"repeated": True})
        
        # Se tudo der certo
        return redirect("login")
    
@csrf_exempt
def login(request: Type[HttpRequest]):
    
    # Se for requisição GET ele retorna a página, se for POST ele reconhece como uma resposta de formulário
    
    if request.method == 'GET':
        
        return render(request, 'login.html')
    
    elif request.method == 'POST':
        
        username:str = request.POST.get('username')
        password:str = request.POST.get('password')

        if not username and password:
            return render(request, 'login.html', {"error": True})

        token:str = LOGIN_MANAGER.login(username, password)

        if token:
            user:dict = Database.getUserByID(LOGIN_MANAGER.getUserByToken(token))

            LOGIN_MANAGER.cache(user["_id"], user["username"], user["name"], user["icon"])

            response:Type[HttpResponse] = redirect('home')
            response.set_cookie('sessionToken', token)
            
            return response
        else:
            return render(request, 'login.html', {'error':True})
    
        

def search(request: Type[HttpRequest]):
    user:dict = LOGIN_MANAGER.recoverCached(LOGIN_MANAGER.getUserByRequest(request))
    if user:
        return render(request, 'search.html', {"logged":True, "user": user})
    else:
        return render(request, 'search.html', {"logged":False})

def searchMedia(request: Type[HttpRequest], category:str, query:str):
    
    res:Type[HttpResponse] = JsonResponse({"result": Database.searchMediaByQuery(category, query)})
    return res

def media(request: Type[HttpRequest], category:str, id:str):
    
    user:dict = LOGIN_MANAGER.recoverCachedByRequest(request)
    
    # Recuperando a mídia
    mediaObj:dict = Database.searchSingleMedia(category, id)
    
    universalMediaId:str = Media.generateMediaId(category, id)
    
    # Cria uma instância no banco se já não houver
    if Database.getMediaByID(universalMediaId) == None:
            ## Cria uma instância no banco caso não exista
            Database.registerMedia(Media(id, category, mediaObj["title"], mediaObj["description"], mediaObj["score"], mediaObj["poster_path"], mediaObj["banner_path"], None, mediaObj["release_year"]))

    # Gerando lista de reviews
    reviews:dict = Database.getReviewsToRenderMedia(category, universalMediaId, user["username"] if user else None)

    # Verificando se está logado
    
    if user:
        
        # Sobrescreve user com o usuário completo pra saber se ele consumiu a obra
        user = Database.getUserByUsername(user["username"])
        
        seen:bool = True if universalMediaId in user["watched"][category] else False
        
        return render(request, 'media.html', {
            "logged":True, 
            "user": user, 
            "seen": seen,
            "media": mediaObj, 
            "reviews":reviews                     
            })
    else:
        return render(request, 'media.html', {"logged":False, "media": mediaObj, "seen": False, "reviews":reviews})

def notfound(request: Type[HttpRequest]):
    # Você realmente quer que eu explique o que isso faz?
    return render(request, 'not-found.html')

@csrf_exempt
def markAsSeen(request: Type[HttpRequest], mediaType:str, mediaID:str):
    """
    Recebe uma requisição de um usuário idealmente logado com um tipo de mídia e seu respectivo id, 
    - Marca a obra na lista de vistos do usuário
    - Adiciona a avaliação no diário dele
    - Adiciona a avaliação do usuário na listas de avaliações da obra
    """
    
    response:Type[HttpResponseNotModified] = HttpResponseNotModified()
    if not request.method == "POST":
        response.headers = {"request-status":"Not POST method"}
        return response
    
    if LOGIN_MANAGER.isLoggedRequest(request):
        
        clientID = LOGIN_MANAGER.getUserByRequest(request)
        
        user:dict = Database.getUserByID(clientID) 
        
        universalMediaId:str = Media.generateMediaId(mediaType, mediaID)
        
        reviewQuality:str = request.POST.get('review-quality')
        reviewText:str = request.POST.get('review-text')
        
        contentReview:dict = {
            "review-quality": reviewQuality if reviewQuality else None,
            "review-text": reviewText if reviewText else None,
        }
        
        # Tentando recuperar review existente
        existingReview:dict = Database.getReviewByID(Review.generateReviewId(user["username"], mediaType, mediaID))
        
        # Se a review já existir
        if existingReview:
            if existingReview['content']["review-quality"] or existingReview['content']["review-text"]:
                existingReview["content"] = contentReview
                Database.editReview(existingReview)
            else:
                Database.deleteReview(existingReview)
                user["watched"][mediaType][mediaID] = False
                Database.refreshUser(user)
            return response
    
        # Adicionando ao diário
        currentMedia:dict = Database.getMediaByID(Media.generateMediaId(mediaType, mediaID))
        
        user["diary"].append({
            "media_id": currentMedia["_id"],
            "realDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "strDate": date.today().strftime("%d/%m/%Y"),
            "name": currentMedia["name"],
            "api_id": currentMedia["api_id"],
            "category": currentMedia["category"],
            "banner_path": currentMedia["bannerPath"],
        })
    
        # Adicionando nas reviews do usuário
        user["watched"][mediaType][universalMediaId] = True if contentReview["review-quality"] or contentReview["review-text"] else False
        
        # Adicionando na tabela de reviews do banco de dados
        if contentReview["review-quality"] or contentReview["review-text"]:
            user["reviewsNumber"] += 1
            review:Type[Review] = Review(user["username"], mediaType, mediaID, contentReview)
            Database.registerReview(review)
        
        # Atualizando perfil do usuário
        Database.refreshUser(user)
        
        # Adicionando nas reviews da mídia
        
        currentMedia["viewsList"].append(user["username"])
        currentMedia["viewsNumber"] = len(currentMedia["viewsList"])
        
        Database.refreshMedia(currentMedia)
        
        return response
    else:
        # Se tentar dar review sem login
        return redirect('login')
    
@csrf_exempt
def editProfile(request: Type[HttpRequest]):
    if LOGIN_MANAGER.isLoggedRequest(request):
        if request.method == "POST":

            name:str = request.POST.get('name')
            bio:str = request.POST.get('bio')
            icon:int = request.POST.get('icon')
            banner:int = request.POST.get('banner')
            
            id = LOGIN_MANAGER.getUserByRequest(request)
            currentUser:dict = Database.getUserByID(id)
            
            currentUser["name"] = name
            currentUser["bio"] = bio
            currentUser["icon"] = icon
            currentUser["banner"] = banner
            
            Database.refreshUser(currentUser)
            
            LOGIN_MANAGER.updateCache(currentUser["_id"], currentUser["username"], currentUser["name"], currentUser["icon"])
            
            response:Type[HttpResponse] = redirect('profile', currentUser["username"])
            
            return response
    
        logged:bool = LOGIN_MANAGER.isLoggedRequest(request)
    
        icons:list = []
        banners:list = []
        
        for i in range(0, len(ICONS_LIST)):
            icons.append(i)
            
        for j in range(0, len(BANNER_LIST)):
            banners.append(j)
        
        currentProfile:dict = Database.getUserByID(LOGIN_MANAGER.getUserByRequest(request))
        
        if currentProfile:
            # Se o perfil existir
            
            return render(request, 'editProfile.html', {"currentProfile":currentProfile, "icons": icons, "banners":banners, "logged": logged})

        else:
            # Se o perfil não existir

            return render(request, 'not-found.html')
    else:
        # Se não for uma request com login
        
        return render(request, "not-found.html")

def logout(request: Type[HttpRequest]):
    id = LOGIN_MANAGER.getUserByRequest(request)
    LOGIN_MANAGER.deleteLoginByCache(id)
    response:Type[HttpResponse] = redirect('home')
    response.delete_cookie('sessionToken')
    return response

@csrf_exempt
def follow(request: Type[HttpRequest], username:str):
    if not LOGIN_MANAGER.isLoggedRequest(request):
        return redirect('login')
    
    userID = LOGIN_MANAGER.getUserByRequest(request)
    
    if LOGIN_MANAGER.recoverCached(userID)["username"] == username:
        # Tentou seguir ele mesmo kkkkkkkkkkkk
        return HttpResponseNotModified()
    
    user:dict = Database.getUserByID(userID)
    followTarget:dict = Database.getUserByUsername(username)
    
    if followTarget["username"] in user["following"]:
        # Usuário já segue o alvo
        return redirect('error', "Ops, parece que você tentou seguir alguém mais de uma vez...") # ! FAZER ROTA DE ERRO (PASSANDO A MENSAGEM COMO PARÂMETRO DE CONTEXTO)
    
    if user and followTarget:
        user["followingCount"] += 1
        user["following"].append(followTarget["username"])
        followTarget["followersCount"] += 1
        followTarget["followers"].append(user["username"])
        
        # Concretizando alterações
        Database.refreshUser(user)
        Database.refreshUser(followTarget)
        
        return HttpResponseNotModified()

@csrf_exempt
def unfollow(request: Type[HttpRequest], username:str):
    if not LOGIN_MANAGER.isLoggedRequest(request):
        return redirect('login')
    
    userID = LOGIN_MANAGER.getUserByRequest(request)
    
    if LOGIN_MANAGER.recoverCached(userID)["username"] == username:
        # Tentou dar unfollow nele mesmo 💔
        return HttpResponseNotModified()
    
    user:dict = Database.getUserByID(userID)
    followTarget:dict = Database.getUserByUsername(username)    
    
    if not followTarget["username"] in user["following"]:
        # Usuário não segue o alvo
        return redirect('login')
    
    if user and followTarget:
        user["followingCount"] -= 1
        user["following"].remove(followTarget["username"])
        followTarget["followersCount"] -= 1
        followTarget["followers"].remove(user["username"])
        
        # Concretizando alterações
        Database.refreshUser(user)
        Database.refreshUser(followTarget)
        
        return HttpResponseNotModified()
    
@csrf_exempt
def removeAsSeen(request: Type[HttpRequest], mediaType:str, mediaID:str):
    if not request.method == "POST":
        return HttpResponseNotModified()
    
    if not LOGIN_MANAGER.isLoggedRequest(request):
        return redirect('login')
    
    userID = LOGIN_MANAGER.getUserByRequest(request)
    user:dict = Database.getUserByID(userID)
    user["watched"][mediaType].pop(Media.generateMediaId(mediaType, mediaID))
    user["watchedNumber"] -= 1
    user["reviewsNumber"] -= 1
    temp:list = []
    for page in user["diary"]:
        if Media.generateMediaId(mediaType, mediaID) == page["media_id"]:
            continue
        temp.append(page)
    user["diary"] = [*temp]
        
    Database.deleteReviewByID(Review.generateReviewId(user["username"], mediaType, mediaID))
    
    media:dict = Database.getMediaByID(Media.generateMediaId(mediaType, mediaID))
    media["viewsList"].remove(user["username"])
    media["viewsNumber"] -= 1

    # Concretizando alterações
    Database.refreshUser(user)
    Database.refreshMedia(media)
    
    return HttpResponseNotModified()

def credits(request: Type[HttpRequest]):
    logged:bool = False
    clientProfile:dict = None
    if LOGIN_MANAGER.isLoggedRequest(request): # Se o cliente estiver logado
        logged = True
        
        clientID = LOGIN_MANAGER.getUserByRequest(request)
        
        clientProfile = LOGIN_MANAGER.recoverCached(clientID)
    return render(request, 'credits.html', {"logged": logged, "user": clientProfile})

@csrf_exempt
def watchlist(request: Type[HttpRequest], category: str, id: str):
    if not LOGIN_MANAGER.isLoggedRequest(request):
        return redirect('login')
    response:Type[HttpResponseNotModified] =  HttpResponseNotModified()
    clientID = LOGIN_MANAGER.getUserByRequest(request)
    user:dict = Database.getUserByID(clientID)
    universalMediaId:str = Media.generateMediaId(category, id)
    if universalMediaId in user["watched"][category]:
        return response
    if universalMediaId in user["watchList"][category]:
        ... # já ta na watchlist
        user["watchList"][category].pop(universalMediaId) # tira da watchlist se tiver
    else:
        ... # nao ta ainda
        user["watchList"][category][universalMediaId] = False # coloca na watchlist se nao tiver
    return response
        
@csrf_exempt
def watching(request: Type[HttpRequest], category: str, id:str):
    if not LOGIN_MANAGER.isLoggedRequest(request):
        return redirect('login')
    response:Type[HttpResponseNotModified] = HttpResponseNotModified()
    clientID = LOGIN_MANAGER.getUserByRequest(request)
    user:dict = Database.getUserByID(clientID)
    universalMediaId:str = Media.generateMediaId(category, id)
    if universalMediaId in user["watched"][category]:
        return response
    if not universalMediaId in user["watchList"][category]:
        return response
    if user["watchList"][category][universalMediaId] == False:
        user["watchList"][category][universalMediaId] == True
    else:
        user["watchList"][category][universalMediaId] == False
        
    return response
    pass # essa rota é pra marcar/desmarcar o que o usuário está vendo/consumindo atualmente