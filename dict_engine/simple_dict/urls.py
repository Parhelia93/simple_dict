from django.urls import path
from .views import *

urlpatterns = [
    path('', SearchWord.as_view(), name='search_word_url'),
    path('register/', RegisterUser.as_view(), name='register_url'),
    path('login/', LoginUser.as_view(), name='login_url'),
    path('logout/', logout_user, name='logout_url'),
    path('user_dict/', ShowUserDict.as_view(), name='user_dict_url'),
    path('create_user_word/', CreateUserWord.as_view(), name='create_user_word_url'),
    path('user_word_detail/<str:slug>', ShowUserWordDetail.as_view(), name='user_word_detail_url'),
    path('user_word_update/<str:slug>', UpdateUserWord.as_view(), name='user_word_detail_update_url')
]
