from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.event_list, name='events'),
    
     
    # 🌟 Register for an event
    path('register/<int:event_id>/', views.register_for_event, name='register_for_event'),

    # 🗳️ Vote for a candidate in an event
    path('vote/<int:event_id>/<int:candidate_id>/', views.vote_for_candidate, name='vote_for_candidate'),

    path('events/<int:event_id>/results/', views.event_results, name='event_results'),
    
    path('<int:event_id>/', views.event_detail, name='event_detail'),
]
