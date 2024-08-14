from django.contrib import admin
from django.urls import path
from . import views  # Import your views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='homepage'),
    path('index/about/', views.about, name='aboutpage'),
    
    path('index/about/data/',views.data,name='datapage'),
    path('data/', views.data, name='data'),
    path('index/data',views.data, name='data'),
    path('about/data/', views.data, name='data'),
    
    path('index/about/index/', views.index, name='homepage'),
    path('predict/', views.predict, name='predict'),
    path('predict/index/', views.index, name='homepage'),
]
