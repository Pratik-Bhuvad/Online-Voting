from django.urls import path, include

urlpatterns = [
    path('', include('pages.urls')),
    path('users/', include('users.urls')),
    path('events/', include('events.urls')),
    path('candidates/', include('candidates.urls')),
]
