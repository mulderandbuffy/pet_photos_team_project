from django.shortcuts import render
from django.http import HttpResponse
from PetPhotos.models import Category
from PetPhotos.forms import CategoryForm

def index(request):
    response = render(request, 'PetPhotos/index.html')
    return response

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
    return render(request, 'PetPhotos/category.html', context=context_dict)


#@login_required    add back when login done
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/PetPhotos/')
        else:
            print(form.errors)
    return render(request, 'PetPhotos/add_category.html', {'form': form})
