from django.urls import path
from PetPhotos import views

app_name= 'PetPhotos'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('like_picture/', views.LikePictureView.as_view(), name='like_picture'),
    path('register/', views.register, name='register'),
    ]
