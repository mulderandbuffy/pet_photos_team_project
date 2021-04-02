from django.contrib import admin
from PetPhotos.models import Pet, UserProfile, Category, Picture, Comment
<<<<<<< HEAD

admin.site.register(UserProfile)


class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')


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

=======

admin.site.register(UserProfile)


class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')


admin.site.register(Pet, PetAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'creation_date')


admin.site.register(Category, CategoryAdmin)


class PictureAdmin(admin.ModelAdmin):
    list_display = ('id', 'rating', 'creator', 'category', 'creation_date')


admin.site.register(Picture, PictureAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'picture', 'creation_date')


admin.site.register(Comment, CommentAdmin)
>>>>>>> f90261c3cccac6d8b3f066d838312082ecfd3acb
