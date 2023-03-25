from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addTasks/', views.AddTasks, name='addTasks'),
    path('fillResults/', views.FillResults, name='fillResults'),
]