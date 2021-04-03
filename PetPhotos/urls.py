from django.urls import path
from PetPhotos import views

app_name= 'PetPhotos'

urlpatterns = [
    path('', views.index, name='index'),
    ]