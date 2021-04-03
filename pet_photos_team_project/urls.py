from django.contrib import admin
from django.urls import path
from django.urls import include
from PetPhotos import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
	  path('PetPhotos/', include('PetPhotos.urls')),
    path('admin/', admin.site.urls),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
