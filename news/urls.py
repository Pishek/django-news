from django.urls import path
from .views import index, get_category,view_news, add_news, register, user_login, user_logout

urlpatterns = [
    #path('', index, name='home'),
    path('', index.as_view(), name='home'),
    path('category/<int:category_id>/', get_category.as_view(), name='category'),
    path('news/<int:news_id>/', view_news.as_view(), name = 'view_news'),
    path('news/add-news/', add_news.as_view(), name = 'add_news'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout')
]

