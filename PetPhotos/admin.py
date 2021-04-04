from django.contrib import admin
from PetPhotos.models import Pet, UserProfile, Category, Picture, Comment


admin.site.register(UserProfile)


class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'slug')


admin.site.register(Pet, PetAdmin)



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'creation_date', 'slug')


admin.site.register(Category, CategoryAdmin)


class PictureAdmin(admin.ModelAdmin):
    list_display = ('id', 'rating', 'creator', 'category', 'creation_date')


admin.site.register(Picture, PictureAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'picture', 'creation_date')


admin.site.register(Comment, CommentAdmin)
