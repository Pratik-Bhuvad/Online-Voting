from django.urls import path
from .views import event_list, vote_event

urlpatterns = [
    path('', event_list, name='events'),
    path('<int:event_id>/vote/', vote_event, name='vote_page'),
    path('vote/<int:event_id>/', vote_event, name='vote_event')
]
