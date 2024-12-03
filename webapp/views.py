from django.shortcuts import render, redirect
from .models import UsersCollection, User, LoginManager
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotModified, JsonResponse
from .modules import TMDB, GoogleBooks, RawgGames, MediaModelSearch, MediaModelPage

LOGIN_MANAGER = LoginManager()

def home(request):
    accessToken = request.COOKIES.get('sessionToken')
    print(request.COOKIES)
    print(accessToken)
    print("LOGIN_MANAGER: {}".format(LOGIN_MANAGER.tokenList))
    if accessToken:
        userID = ''
        try:
            userID = LOGIN_MANAGER.tokenList[accessToken]
        except:
            return render(request, 'home.html', {"logged":False})
        
        user = UsersCollection.find_one({"_id": userID})
        return render(request, 'home.html', {"logged":True, "user": user})
    else:
        return render(request, 'home.html', {"logged":False})
        #return redirect('cadastro')

# Create your views here.

def profile(request, username):
    accessToken = request.COOKIES.get('sessionToken')
    print("LOGIN_MANAGER: {}".format(LOGIN_MANAGER.tokenList))
    currentProfile = UsersCollection.find_one({"username": username})
    print(accessToken)
    
    selfProfile = False
    if accessToken in LOGIN_MANAGER.tokenList: # SE ESTIVER LOGADO
        clientID = LOGIN_MANAGER.tokenList[accessToken]
        print(LOGIN_MANAGER.isLogged(clientID)) # Consegue identificar se o perfil que está sendo acessado é o mesmo do usuário logado
        selfProfile = True if currentProfile["_id"] == clientID else False
        print("\n\n{}\n{}\n\n".format(currentProfile["_id"], clientID))
        currentProfile["user"] = LOGIN_MANAGER.cacheLogged[clientID]

    if currentProfile:  # SE O PERFIL EXISTIR
        currentProfile["selfProfile"] = selfProfile
        currentProfile["logged"] = accessToken in LOGIN_MANAGER.tokenList
        print(currentProfile)
        return render(request, 'profile.html', currentProfile) # podia ter um terceiro argumento com um dicionario com as variaveis pra passas por meio de {{uma chave}}

    else:

        return render(request, 'not-found.html')

@csrf_exempt
def cadastro(request):
    print() # Retorna None se n tem nenhum
    print(request)
    if request.method == 'GET':
        
        return render(request, 'cadastro.html')
    
    elif request.method == 'POST':
        if UsersCollection.find_one({"username": "{}".format(request.POST.get('username'))}) == None:
            pass # cria
            newUser = User(
                request.POST.get('name'),
                request.POST.get('username'),
                request.POST.get('email'),
                request.POST.get('password')
            )
            UsersCollection.insert_one(newUser.toDict())
        else :
            pass # nao cria
        print(request.POST.get('name'))
        return HttpResponse("Success")
        # UsersCollection.insert_one()
    
@csrf_exempt
def login(request):
    print(request)
    if request.method == 'GET':
        
        return render(request, 'login.html', {'error':None})
    
    elif request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        token = LOGIN_MANAGER.login(username, password)

        if token:
            user = UsersCollection.find_one({"_id": LOGIN_MANAGER.tokenList[token]})

            LOGIN_MANAGER.cacheLogged[user["_id"]] = {
                "username": user["username"],
                "name": user["name"],
                "icon": user["icon"]
            }

            response = redirect('home')

            response.set_cookie('sessionToken', token)
            print(LOGIN_MANAGER.tokenList)
            return response
        else:
            print(LOGIN_MANAGER.tokenList)
            return render(request, 'login.html', {'error':True})
    
        

def search(request):
    accessToken = request.COOKIES.get('sessionToken')
    if accessToken:
        userID = ''
        try:
            userID = LOGIN_MANAGER.tokenList[accessToken]
        except:
            return render(request, 'search.html', {"logged":False})
        
        user = UsersCollection.find_one({"_id": userID})
        return render(request, 'search.html', {"logged":True, "user": user})
    else:
        return render(request, 'search.html', {"logged":False})

def searchMedia(request, category, query):
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
                    result["release_date"]
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
                    result["first_air_date"]
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
                    result["first_air_date"]
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
    res = JsonResponse({"result":queryResult})
    return res

def media(request, category, id):
    # Recuperando a mídia
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

    # Verificando se está logado
    accessToken = request.COOKIES.get('sessionToken')
    if accessToken:
        userID = ''
        try:
            userID = LOGIN_MANAGER.tokenList[accessToken]
        except:
            return render(request, 'media.html', {"logged":False, "media": mediaObj, "seen": False})
        
        user = UsersCollection.find_one({"_id": userID})
        
        universalMediaId = "{}_{}".format(category, id)
        
        seen = True if universalMediaId in user["watched"][category] else False
        return render(request, 'media.html', {"logged":True, "user": user, "seen": seen,"media": mediaObj})
    else:
        return render(request, 'media.html', {"logged":False, "media": mediaObj, "seen": False})

def notfound(request):
    return render(request, 'not-found.html')


# ! EM DESENVOLVIMENTO
@csrf_exempt
def markAsSeen(request, mediaType, mediaID):
    """
    Recebe uma requisição de um usuário idealmente logado com um tipo de mídia e seu respectivo id, 
    - Marca a obra na lista de vistos do usuário
    - Adiciona a avaliação no diário dele
    - Adiciona a avaliação do usuário na listas de avaliações da obra
    """
    accessToken = request.COOKIES.get('sessionToken')
    response = HttpResponseNotModified()
    if not request.method == "POST":
        response.headers = {"request-status":"Not POST method"}
        return response
    print(request.POST)
    if accessToken:
        userID = ''
        try:
            userID = LOGIN_MANAGER.tokenList[accessToken]
        except:
            response.headers = {"request-status": "Invalid Token"}
            return redirect(login)
        
        user = UsersCollection.find_one({"_id": userID})
        
        universalMediaId = "{}_{}".format(mediaType, mediaID)
        
        user["watched"][mediaType].append(universalMediaId)
        UsersCollection.replace_one({"_id": user["_id"]}, user)
        print("mediaType: {}".format(mediaType))
        print("mediaID: {}".format(mediaID))
        print("universalMediaId: {}".format(universalMediaId))
        response.headers = {"request-status": "Accepted"}
        return response
    else:
        response.headers["request-status"] = "Without Token"
        return redirect(login)
    

def editProfile(request):
    # accessToken = request.COOKIES.get('sessionToken')
    # if accessToken:
    #     userID = ''
    #     try:
    #         userID = LOGIN_MANAGER.tokenList[accessToken]
    #     except:
    #         # logged false
    #         return render(request, 'home.html', {"logged":False})
        
    #     user = UsersCollection.find_one({"_id": userID})
    #     # logged true
    #     return render(request, 'home.html', {"logged":True, "user": user})
    # else:
    #     # logged false
    #     return render(request, 'home.html', {"logged":False})
    accessToken = request.COOKIES.get('sessionToken')
    
    if not accessToken or not accessToken in LOGIN_MANAGER.tokenList:
        return render(request, 'not-found.html')
    
    currentProfile = UsersCollection.find_one({"_id": LOGIN_MANAGER.tokenList[accessToken]})
    
    if currentProfile:  # SE O PERFIL EXISTIR
        return render(request, 'editProfile.html', currentProfile) # podia ter um terceiro argumento com um dicionario com as variaveis pra passas por meio de {{uma chave}}

    else:

        return render(request, 'not-found.html')