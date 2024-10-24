from django.shortcuts import render
from .models import UsersCollection, User
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse




# Create your views here.

def profile(request, username):
    currentUser = UsersCollection.find_one({"username": username})
    
    return render(request, 'profile.html', currentUser) # podia ter um terceiro argumento com um dicionario com as variaveis pra passas por meio de {{uma chave}}

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
    
