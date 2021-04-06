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
    path('view_pet_profile/<slug:pet_slug>/', views.view_pet_profile, name='view_pet_profile'),
    path('view_picture/<slug:id>/', views.view_picture, name='view_picture'),
    path('search_category/', views.search_category, name='search_category'),
    path('like/<slug:id>/', views.like_view, name='like_post'),
    path('delete/<slug:pic_id>/<slug:com_id>', views.del_comment, name='del_comment'),
    path('delete_pet/<slug:pet_id>/<slug:own_id>', views.del_pet, name='del_pet'),
    path('delete_pic/<slug:pic_id>/<slug:cat_id>', views.del_pic, name='del_pic'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('trending/', views.trending, name='trending')
]
