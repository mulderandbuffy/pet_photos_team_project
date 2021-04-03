from django.shortcuts import render
from django.http import HttpResponse
from PetPhotos.models import Category, Pet, User
from PetPhotos.forms import CategoryForm, PetForm
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required



# Create your views here.
def index(request):
    response = render(request, 'PetPhotos/index.html')
    return response

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pictures = Picture.objects.filter(category=category)
        context_dict['pictures'] = pictures
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pictures'] = None
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

#@login_required
class LikePictureView(View):
    #@method_decorator(login_required)
    def get(self, request):
        picture_id = request.GET['picture_id']
        try:
            picture = Picture.objects.get(id=int(picture_id))
        except Picture.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        picture.rating = picture.rating + 1
        picture.save()

        return HttpResponse(picture.rating)

#@login_required
def add_pet(request):
    #POST?
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)

        if form.is_valid:
            pet = form.save(commit=False)
            pet.owner = UserProfile.objects.get(request.user)

            if 'picture' in request.FILES:
                pet.picture = request.FILES['picture']

        else:
            print(form.errors)

        pet.save()
    return render(request, 'PetPhotos/addpet.html', {'form':form})


