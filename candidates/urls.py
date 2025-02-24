from django.urls import path
from . import views

urlpatterns = [
    path('', views.candidate_list, name='candidates'),
    path('<int:candidate_id>/', views.candidate_detail, name='candidate_detail'),
]
