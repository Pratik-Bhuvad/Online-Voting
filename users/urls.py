from django.urls import path
from .views import signup, user_login, user_logout , user_dashboard

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
     path('dashboard/', user_dashboard, name='dashboard'), 
]
