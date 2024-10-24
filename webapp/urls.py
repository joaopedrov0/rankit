from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:username>/', views.profile, name='profile'),
    # path('rota', views.qualFunçãoDeViews, name="nome pro formulário saber a url q ele tem q mandar as parada")
    path('cadastro', views.cadastro, name='cadastro')
]