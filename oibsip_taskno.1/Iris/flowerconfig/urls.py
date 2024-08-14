from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index_homepage'),
    path('index/about/', views.about, name='index_about'),
    path('index/about/data/', views.data, name='index_about_data'),
    path('index/data/', views.data, name='index_data'),
     path('index/data/index', views.index, name='index_data'),
    
    path('about/', views.about, name='aboutpage'),
    
    path('data/', views.data, name='data'),
    path('recommend/', views.recommend, name='recommend'),
]
