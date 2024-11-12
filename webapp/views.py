from django.shortcuts import render, redirect
from .models import UsersCollection, User, LoginManager
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

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

def media(request):
    accessToken = request.COOKIES.get('sessionToken')
    if accessToken:
        userID = ''
        try:
            userID = LOGIN_MANAGER.tokenList[accessToken]
        except:
            return render(request, 'media.html', {"logged":False})
        
        user = UsersCollection.find_one({"_id": userID})
        return render(request, 'media.html', {"logged":True, "user": user})
    else:
        return render(request, 'media.html', {"logged":False})

def notfound(request):
    return render(request, 'not-found.html')
