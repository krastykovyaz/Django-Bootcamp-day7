from articles.views import Home, LoginPage, Articles, Publications, Detail, Logout, Favourites
from django.urls import path
from articles.views import register

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('register/', register, name='register'),
    path('favourites/', Favourites.as_view(), name='favourites'),
    path('articles/', Articles.as_view(), name='articles'),
    path('login/', LoginPage.as_view(), name='login'),
    path('publications/', Publications.as_view(), name='publications'),
    path('article/<int:pk>/', Detail.as_view(), name='article-detail'),
    path('logout/', Logout.as_view(), name='logout'),
]