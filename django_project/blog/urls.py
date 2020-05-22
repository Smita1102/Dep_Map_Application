from django.urls import path
from . import views


urlpatterns = [
   
    path('home/', views.home,name='modules-home'),
    path('about/', views.about,name='modules-about'),
    path('mcq/', views.QuestionView.as_view(), name='mcq'),
    path('restart', views.restart, name='restart'),
    path('index/', views.index, name='index'),

    


]   
