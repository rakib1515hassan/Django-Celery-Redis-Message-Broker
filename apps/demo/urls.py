from django.urls import path
from apps.demo import views

app_name = 'demo'


urlpatterns = [
    path('result/', views.test, name='test'),
    path('result/<str:task_id>/', views.result_view, name='result_view'),
]