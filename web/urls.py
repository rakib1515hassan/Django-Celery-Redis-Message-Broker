from django.urls import path, include


urlpatterns = [
    path('', include('web.index.urls',  namespace='index')),
    
]