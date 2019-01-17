from django.urls import path

from reg_log.views import *

app_name = 'reg_log'
urlpatterns = [
    path('register/', register, name='reg'),
    path('login/', login, name='login')
]