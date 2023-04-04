from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addTasks/', views.AddTasks, name='addTasks'),
    path('fillResults/', views.FillResults, name='fillResults'),
    path('login/', views.Login, name='Login'),
    path('register/', views.Register, name='Register'),
    path('logout/', views.LogOut, name='Logout'),
    path('user/<str:username>/', views.DisplayUser, name='User'),

]
