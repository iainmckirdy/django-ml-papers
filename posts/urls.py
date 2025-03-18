from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('posts/<str:date>', views.post),
    path('about/', views.about),

]