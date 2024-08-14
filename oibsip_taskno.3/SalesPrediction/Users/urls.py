from django.urls import path
from .import views

urlpatterns=[
    path('',views.index,name='homepage'),
    path('about',views.about,name='aboutpage'),
    path('products',views.products,name='productspage'),
    path('register',views.register,name='registerpage'),
    path('login',views.login,name='loginpage'),
    path('logout',views.logout,name='logoutpage'),
    path('data',views.data,name='datapage'),
    path('predict',views.predict,name='predictpage')
]