from django.urls import path, include
from web.index import views

app_name = 'index'

urlpatterns = [
    path('', views.home, name='index_page'),

]