from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:username>/', views.profile, name='profile'),
    # path('rota', views.qualFunçãoDeViews, name="nome pro formulário saber a url q ele tem q mandar as parada")
    path('cadastro', views.cadastro, name='cadastro'),
    path('login', views.login, name='login'),
    path('search', views.search, name='search'),
    path('', views.home, name='home'),
    path('media/<str:category>/<str:id>', views.media, name='media'),
    path('not-found', views.notfound, name='notfound'),
    path('markAsSeen/<str:mediaType>/<str:mediaID>', views.markAsSeen, name='markAsSeen'),
    path('searchMedia/<str:category>/<str:query>', views.searchMedia, name='searchMedia'),
]