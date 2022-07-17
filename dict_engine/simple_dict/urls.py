from django.urls import path
from .views import *

urlpatterns = [
    path('', SearchWord.as_view(), name='search_word_url'),
    path('register/', RegisterUser.as_view(), name='register_url'),
    path('login/', LoginUser.as_view(), name='login_url'),
    path('logout/', logout_user, name='logout_url'),
    path('user_dict/', ShowUserDict.as_view(), name='user_dict_url')
]
