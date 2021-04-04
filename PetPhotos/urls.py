from django.urls import path
from PetPhotos import views

app_name = 'PetPhotos'

urlpatterns = [
    path('', views.index, name='index'),
    path('user_profiles/', views.user_profiles, name='user_profiles'),
    path('user_profile/<username>/', views.user_profile, name='user_profile'),
    path('categories/', views.categories, name='categories'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_pet/', views.add_pet, name='add_pet'),
    path('add_picture/', views.add_picture, name='add_picture'),
    path('viewpetprofile/<slug:pet_slug>/', views.viewpetprofile, name='viewpetprofile'),
    # path('like_picture/', views.LikePictureView.as_view(), name='like_picture'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
<<<<<<< HEAD
    path('restricted/', views.restricted, name='restricted'),
    ]
=======
]
>>>>>>> origin/main
