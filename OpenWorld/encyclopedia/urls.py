from django.urls import path
from .views import index, article, create_article, get_all_actricles, detail

urlpatterns = [
    path('', index, name='home'),
    path('/articles', article, name='articles'),
    path('/create_article', create_article, name='create_article'),
    path('/get_articles', get_all_actricles, name='get_articles'),
    path('/detail/<str:article_id>', detail, name='article_detail')
]