from django.urls import path
from PetPhotos import views

app_name= 'petphotos'

urlpatterns = [
    path('', views.index, name='index'),
    ]