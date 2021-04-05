from django import template
from PetPhotos.models import Category

register = template.Library()

@register.inclusion_tag('PetPhotos/categorylist.html')
def get_category_list(current_category=None):
    return {'categories': Category.objects.all(),
            'current_category': current_category}
